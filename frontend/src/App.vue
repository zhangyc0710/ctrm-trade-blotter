<template>
  <div class="app-container">
    <h1>商品交易看板</h1>
    
    <!-- 交易表单 -->
    <el-card class="trade-form">
      <h2>新增交易</h2>
      <el-form :model="tradeForm" :rules="rules" ref="formRef">
        <el-form-item label="商品名称" prop="commodity">
          <el-input v-model="tradeForm.commodity" placeholder="例如：原油" />
        </el-form-item>
        
        <el-form-item label="交易类型" prop="type">
          <el-radio-group v-model="tradeForm.type">
            <el-radio value="Buy">买入</el-radio>
            <el-radio value="Sell">卖出</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="数量(吨)" prop="quantity">
          <el-input-number v-model="tradeForm.quantity" :min="0.1" :step="0.1" @change="handleQuantityChange" />
        </el-form-item>
        
        <el-form-item label="价格(美元/吨)" prop="price">
          <el-input-number v-model="tradeForm.price" :min="0.01" :step="0.01" :precision="2" @change="handlePriceChange" />
        </el-form-item>
        
        <el-button type="primary" @click="submitTrade">提交交易</el-button>
      </el-form>
    </el-card>

    <!-- 交易表格 -->
    <el-card class="trade-table">
      <h2>交易记录</h2>
      <el-table :data="trades" style="width: 100%">
        <el-table-column prop="commodity" label="商品" />
        <el-table-column label="类型">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'Buy' ? 'success' : 'danger'">
              {{ scope.row.type === 'Buy' ? '买入' : '卖出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量(吨)" />
        <el-table-column label="价格(美元)">
          <template #default="scope">${{ scope.row.price.toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="名义价值(美元)">
          <template #default="scope">${{ (scope.row.quantity * scope.row.price).toFixed(2) }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 表单数据
const tradeForm = ref({
  commodity: '',
  type: 'Buy',
  quantity: 1,
  price: 0.01
})

// 处理数量变化
const handleQuantityChange = (value) => {
  tradeForm.value.quantity = Number(value);
  console.log('数量已更新为:', tradeForm.value.quantity, '类型:', typeof tradeForm.value.quantity);
}

// 处理价格变化
const handlePriceChange = (value) => {
  tradeForm.value.price = Number(value);
  console.log('价格已更新为:', tradeForm.value.price, '类型:', typeof tradeForm.value.price);
}

// 监控tradeForm变化
watch(tradeForm, (newValue) => {
  console.log('tradeForm变化:', newValue);
  console.log('quantity类型:', typeof newValue.quantity, 'isArray:', Array.isArray(newValue.quantity));
  console.log('price类型:', typeof newValue.price, 'isArray:', Array.isArray(newValue.price));
}, { deep: true });

// 表单规则
const rules = { 
  commodity: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' },
    { validator: (rule, value, callback) => {
        console.log('验证数量:', value, '类型:', typeof value);
        if (typeof value !== 'number' || isNaN(value)) {
          callback(new Error('数量必须是数字'));
        } else if (value < 0.1) {
          callback(new Error('数量不能小于0.1'));
        } else {
          callback();
        }
      }, trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { validator: (rule, value, callback) => {
        console.log('验证价格:', value, '类型:', typeof value);
        if (typeof value !== 'number' || isNaN(value)) {
          callback(new Error('价格必须是数字'));
        } else if (value < 0.01) {
          callback(new Error('价格不能小于0.01'));
        } else {
          callback();
        }
      }, trigger: 'blur' }
  ]
}

// 交易列表
const trades = ref([])
const formRef = ref()

// 加载交易数据
const loadTrades = async () => {
  try {
    const response = await axios.get('http://localhost:8000/trades')
    trades.value = response.data
  } catch (error) {
    ElMessage.error('加载交易失败')
  }
}

// 提交交易
const submitTrade = async () => {
      try {
        // 确保数量和价格是数字类型
        tradeForm.value.quantity = Number(tradeForm.value.quantity);
        tradeForm.value.price = Number(tradeForm.value.price);
        
        // 验证表单
        await formRef.value.validate()
    
    // 调试：查看tradeForm的结构
    console.log('提交前tradeForm.value:', tradeForm.value);
    console.log('提交前quantity类型:', typeof tradeForm.value.quantity, 'isArray:', Array.isArray(tradeForm.value.quantity));
    console.log('提交前price类型:', typeof tradeForm.value.price, 'isArray:', Array.isArray(tradeForm.value.price));

    // 增强类型转换逻辑
    const formattedTrade = {
      ...tradeForm.value,
      quantity: Array.isArray(tradeForm.value.quantity) ? 
        (tradeForm.value.quantity.length > 0 ? Number(tradeForm.value.quantity[0]) : 0) : 
        (typeof tradeForm.value.quantity === 'string' ? parseFloat(tradeForm.value.quantity) : Number(tradeForm.value.quantity)),
      price: Array.isArray(tradeForm.value.price) ? 
        (tradeForm.value.price.length > 0 ? Number(tradeForm.value.price[0]) : 0) : 
        (typeof tradeForm.value.price === 'string' ? parseFloat(tradeForm.value.price) : Number(tradeForm.value.price))
    };

    // 调试：查看转换后的值
    console.log('转换后的formattedTrade:', formattedTrade);
    console.log('转换后quantity类型:', typeof formattedTrade.quantity);
    console.log('转换后price类型:', typeof formattedTrade.price);
    // 提交数据
    await axios.post('http://localhost:8000/trades', formattedTrade)
    
    // 重置表单
    formRef.value.resetFields()
    tradeForm.value = { commodity: '', type: 'Buy', quantity: 1, price: 0.01 }
    
    // 刷新数据
    await loadTrades()
    ElMessage.success('交易提交成功！')
  } catch (error) {
    console.error('提交交易错误详情:', error);
    if (error.response) {
      ElMessage.error(`提交失败：${error.response.status} ${error.response.data?.detail || '请求体验证失败'}`)
    } else if (error.request) {
      ElMessage.error('提交失败：无响应，请检查后端是否启动')
    } else if (error instanceof Error) {
      ElMessage.error('提交失败：' + error.message)
    } else {
      ElMessage.error('提交失败：未知错误，' + JSON.stringify(error))
    }
  }
}

// 页面加载时获取数据
onMounted(() => {
  loadTrades()
})
</script>

<style>
.app-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
}
.trade-form, .trade-table {
  margin-bottom: 30px;
}
h1, h2 {
  color: #333;
}
</style>