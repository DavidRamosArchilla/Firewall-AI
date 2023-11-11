<template>
    <div> {{ tableData[0] }} </div>
    <div>
      <DataTable :value="tableData"> 
        <Column field="field1" header="Header 1"></Column>
        <Column field="field2" header="Header 2"></Column>
      </DataTable>
    </div>
  </template>
  
  <script>
  // import { ref, onMounted } from 'vue';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import 'primevue/resources/primevue.min.css';
  import 'primevue/resources/themes/saga-blue/theme.css';
//   import 'primeicons/primeicons.css';
  
  export default {
    data() {
        return {
          tableData: [],
          prueba: []
        };
    },
    components: {
      DataTable,
      Column,
    },
    mounted() {
      this.prueba = [
        { field1: "Value1", field2: "Value2" },
        { field1: "Value3", field2: "Value4" },
        // Add more rows as needed
      ];
      const fetchData = () => {
        fetch('http://localhost:5000/get_data') // Replace with your server URL
          .then((response) => response.json())
          .then((data) => {
            // tableData.value = data;
            this.tableData = data;
            // this.tableData = this.tableData.concat(data);
            console.log('data:')
            console.log(data);
            console.log(this.tableData);
            console.log(this.prueba);
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
  
      };
      fetchData();
      // Periodically fetch data every 5 seconds (adjust as needed)
      setInterval(fetchData, 5000);
    //   console.log(this.prueba);
    },
    
  };
  </script>