<template>
  <div class="container">
    <h1 class="title">Yay Bill Order Processor</h1>
    
    <el-card class="upload-card">
      <template #header>
        <span>Upload Order Data</span>
      </template>
      
      <el-input
        v-model="jsonInput"
        type="textarea"
        :rows="8"
        placeholder="Paste JSON content here"
        style="margin-bottom: 20px;"
      />

      <el-button
        class="el-upload__text"
        @click="processJsonInput"
        style="margin-bottom: 30px; color: #409EFF; border-color: #409EFF; background-color: #ecf5ff;"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div>Process JSON</div>
      </el-button>

      <el-upload
        class="upload-demo"
        drag
        :auto-upload="false"
        :show-file-list="false"
        accept=".json"
        :on-change="handleFileUpload"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            Upload your JSON file containing order data
          </div>
        </template>
      </el-upload>
    </el-card>

    <el-card v-if="orderStats" class="stats-card">
      <template #header>
        <span>Order Statistics</span>
      </template>
      
      <div class="stats-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Total Orders">
            {{ orderStats.totalOrders }}
          </el-descriptions-item>
          <el-descriptions-item label="Total Amount">
            ¥{{ orderStats.totalAmount.toFixed(2) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>

    <el-card v-if="orderData.length > 0" class="data-card">
      <template #header>
        <span>Order Details</span>
        <el-button 
          type="success" 
          size="small" 
          @click="exportToExcel"
          style="margin-left: 20px;"
        >
          Export to Excel
        </el-button>
      </template>
      
      <el-table
        :data="orderData"
        stripe
        style="width: 100%"
        max-height="500"
      >
        <el-table-column
          prop="orderId"
          label="Order ID"
          width="200"
          fixed
        />
        <el-table-column
          prop="totalBaseAmount"
          label="Amount"
          width="120"
        />
        <el-table-column
          prop="status"
          label="Status"
          width="120"
        />
        <el-table-column
          prop="createTime"
          label="Create Time"
          width="200"
        />
        <el-table-column
          prop="updateTime"
          label="Update Time"
          width="200"
        />
        <el-table-column
          prop="currency"
          label="Currency"
          width="100"
        />
        <el-table-column
          prop="paymentMethod"
          label="Payment Method"
          width="150"
        />
        <el-table-column
          prop="buyerId"
          label="Buyer ID"
          width="150"
        />
        <el-table-column
          prop="sellerId"
          label="Seller ID"
          width="150"
        />
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { UploadFilled } from '@element-plus/icons-vue';
import { ref } from 'vue';
import * as XLSX from 'xlsx';
import { prepareExcelData, processOrderData } from './utils/dataProcessor';

export default {
  name: 'App',
  components: {
    UploadFilled
  },
  setup() {
    const orderData = ref([])
    const orderStats = ref(null)
    const jsonInput = ref('')
    
    const handleFileUpload = async (file) => {
      try {
        const content = await readFileAsText(file.raw)
        const jsonData = JSON.parse(content)
        
        // Assuming the data structure follows the Python script's expectation
        // where the orders are in the 'rows' property
        let orders = []
        if (jsonData.rows) {
          orders = jsonData.rows
        } else {
          // If the root contains the orders directly
          orders = Array.isArray(jsonData) ? jsonData : [jsonData]
        }
        
        // Process the order data using utility function
        const result = processOrderData(orders)
        orderData.value = result.orders
        orderStats.value = result.stats
      } catch (error) {
        console.error('Error processing file:', error)
        alert('Error processing file: ' + error.message)
      }
    }
    
    const processJsonInput = () => {
      try {
        if (!jsonInput.value.trim()) {
          alert('Please enter valid JSON content')
          return
        }

        const jsonData = JSON.parse(jsonInput.value)
        let orders = []
        
        if (jsonData.rows) {
          orders = jsonData.rows
        } else {
          orders = Array.isArray(jsonData) ? jsonData : [jsonData]
        }

        const result = processOrderData(orders)
        orderData.value = result.orders
        orderStats.value = result.stats
      } catch (error) {
        console.error('Error processing JSON input:', error)
        alert('Invalid JSON format: ' + error.message)
      }
    }
    
    const readFileAsText = (file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => resolve(reader.result)
        reader.onerror = () => reject(reader.error)
        reader.readAsText(file, 'utf-8')
      })
    }
    
    const exportToExcel = () => {
      if (orderData.value.length === 0) return
      
      // Prepare data for Excel export with summary row
      const excelData = prepareExcelData(orderData.value, orderStats.value)
      
      const ws = XLSX.utils.json_to_sheet(excelData)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Orders')
      
      // Export the Excel file
      XLSX.writeFile(wb, 'yay_orders.xlsx')
    }
    
    return {
      orderData,
      orderStats,
      handleFileUpload,
      processJsonInput,
      exportToExcel,
      jsonInput
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  text-align: center;
  color: #409EFF;
  margin-bottom: 30px;
}

.upload-card {
  margin-bottom: 20px;
}

.stats-card {
  margin-bottom: 20px;
}

.stats-content {
  padding: 10px 0;
}

.data-card {
  margin-top: 20px;
}

.el-table {
  margin-top: 20px;
}
</style>
