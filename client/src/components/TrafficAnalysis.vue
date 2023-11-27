<template>
    <div class="chart-container">
        <div class="chart-item">
            <Chart type="bar" :data="barchartData" :options="chartOptions"/>
        </div>
        <div class="chart-item">
            <Chart type="line" :data="linechartData" :options="chartOptions"/>
        </div>
    </div>
</template>

<script>
import Chart from 'primevue/chart';

export default {
    data() {
        return {
            barchartData: null,
            chartOptions: null,
            linechartData: null,
        };
    },
    components: {
        Chart
    },
    mounted() {
        this.setChartsData();
        this.chartOptions = this.setChartOptions();
    },
    methods: {
        setChartsData() {
            fetch('/get_data')
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                const processedBarchartData = this.processFlowDataBarchart(data);
                const processedLinechartData = this.processFlowDataLinechart(data);
                const lineChartDatasets = this.getLineChartDatasets(processedLinechartData);
                this.barchartData = {
                        // labels: ['Q1', 'Q2', 'Q3', 'Q4'],
                        labels: Object.keys(processedBarchartData),
                        datasets: [
                            {
                                label: 'Flows',
                                // data: [540, 325, 702, 620],
                                data: Object.values(processedBarchartData),
                                backgroundColor: ['rgba(255, 159, 64, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(153, 102, 255, 0.2)'],
                                borderColor: ['rgb(255, 159, 64)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)', 'rgb(153, 102, 255)'],
                                borderWidth: 1
                            }
                        ]
                    };
                this.linechartData = {
                    labels: Array.from({ length: data.length + 1 }, (_, index) => index),
                    datasets: lineChartDatasets
                };
            });
        },
        processFlowDataBarchart(predictedData) {
            let data = {};

            for (let i = 0; i < predictedData.length; i++) {
                let flow = predictedData[i];
                let flowType = flow['type'];

                if (!(flowType in data)) {
                    data[flowType] = 1;
                } else {
                    data[flowType] += 1;
                }
            }

            // Assuming you have a jsonify function, use it to convert the data to JSON
            return data;
        },
        processFlowDataLinechart(predictedData){
            let data = {
                'BENIGN': [0],
                'LDAP': [0],
                'MSSQL': [0],
                'UDP': [0],
                'Syn': [0],
            }
            for (let i = 0; i < predictedData.length; i++) {
                let flow = predictedData[i];
                let flowType = flow['type'];
                for (var key in data) {
                    const lastElement = data[key][data[key].length - 1]
                    if(key === flowType)
                        data[key].push(lastElement + 1)
                    else
                        data[key].push(lastElement)
                }
            }
            return data;
        },
        getLineChartDatasets(data){
            let datasets = [];
            for(var key in data){
                datasets.push({
                    label: key,
                    fill: false,
                    data: data[key],
                    // borderColor: 'rgb(255, 159, 64)',
                    // borderColor: ['rgb(255, 159, 64)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)', 'rgb(153, 102, 255)'],
                    tension: 0.4
                });
            }
            return datasets;
        },
        setChartOptions() {
            const documentStyle = getComputedStyle(document.documentElement);
            const textColor = documentStyle.getPropertyValue('--text-color');
            const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
            const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

            return {
                // maintainAspectRatio: false,
                // aspectRatio: 0.6,
                plugins: {
                    legend: {
                        labels: {
                            color: textColor
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: textColorSecondary
                        },
                        grid: {
                            color: surfaceBorder
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: textColorSecondary
                        },
                        grid: {
                            color: surfaceBorder
                        }
                    }
                }
            };
        }
    }
};
</script>
<style scoped>
.chart-container {
    display: flex;
    justify-content: space-between;
}

.chart-item {
    flex: 1;
    margin-right: 10px; /* Adjust margin as needed */
    height: 100vh;
}
</style>