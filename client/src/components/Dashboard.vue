<template>
    <!-- <div> {{ tableData[0] }} </div> -->
    <div>
      <DataTable v-model:filters="filters" :value="tableData" ref="dt" paginator :rows="10" :rowsPerPageOptions="[10, 20, 50, 100]" filterDisplay="row"
            :globalFilterFields="['name', 'country.name', 'representative.name', 'status']" > 
        <template #header>
          <div class="flex justify-content-between">
              <Button type="button" icon="pi pi-filter-slash" label="Clear"  @click="clearFilter()" />
          </div>
        </template>
        <template #empty> No data found. </template>
        <template #loading> Loading traffic data. Please wait. </template>
        <template #paginatorstart>
        </template>
        <template #paginatorend>
            <Button type="button" icon="pi pi-download" outlined label="Download" @click="exportCSV($event)"/>
        </template>
        <Column field="timestamp" header="Timestamp" sortable style="min-width: 10rem">
          <template #body="{ data }">
              {{ data.timestamp }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
              <InputText v-model="filterModel.value" type="date" @input="filterCallback()" class="p-column-filter"/>
          </template>
        </Column>
        <Column field="src_ip" header="Source IP" style="min-width: 12rem">
          <template #body="{ data }">
              {{ data.src_ip }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
              <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search by IP"/>
          </template>
        </Column>
        <Column field="dst_ip" header="Destination IP" style="min-width: 12rem">
          <template #body="{ data }">
              {{ data.dst_ip }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
              <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search by IP"/>
          </template>
        </Column>
        <Column field="confidence" header="Confidence" sortable ></Column>
        <Column field="type" header="Type">
          <template #body="{ data }">
              <Tag :value="data.type" :severity="getSeverity(data.type)" />
          </template>
          <template #filter="{ filterModel, filterCallback }">
              <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="attack_types" placeholder="Select One" class="p-column-filter" style="min-width: 12rem" :showClear="true">
                  <template #option="slotProps">
                      <Tag :value="slotProps.option" :severity="getSeverity(slotProps.option)" />
                  </template>
              </Dropdown>
          </template>
        </Column>
      </DataTable>
    </div>
  </template>
  
  <script>
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import InputText from 'primevue/inputtext';
  import Dropdown from 'primevue/dropdown';
  import Button from 'primevue/button';
  import Calendar from 'primevue/calendar';
  import Tag from 'primevue/tag';
  import { FilterMatchMode } from 'primevue/api'; 
  
  export default {
    data() {
        return {
          tableData: [],
          filters: null,
          attack_types: ['BENIGN', 'LDAP', 'MSSQL', 'UDP', 'Syn'],
        };
    },
    components: {
      DataTable,
      Column,
      InputText,
      Tag,
      Dropdown,
      Button,
      Calendar
    },
    created() {
        this.initFilters();
    },
    mounted() {
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
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
  
      };
      fetchData();
      // Periodically fetch data every 5 seconds (adjust as needed)
      setInterval(fetchData, 5000);
    },
    methods: {
      getSeverity(type){
        if(type === 'BENIGN')
          return 'success';
        else
        return 'danger'; 
      },
      clearFilter(){
        this.initFilters();
      },
      initFilters(){
        this.filters = {
                src_ip: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
                dst_ip: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
                type: { value: null, matchMode: FilterMatchMode.EQUALS },
                timestamp: { value: null, matchMode: FilterMatchMode.CONTAINS },
            }
      },
      exportCSV() {
            this.$refs.dt.exportCSV();
        }
    },
    
  };
  </script>