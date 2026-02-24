/**
 * Utility functions for processing order data
 */

/**
 * Processes raw order data and calculates statistics
 * @param {Array} orders - Array of order objects
 * @returns {Object} Object containing processed data and statistics
 */
export function processOrderData(orders) {
  // Calculate stats
  const totalAmount = orders.reduce((sum, order) => {
    // Convert amount to number, handling string values
    const amount = typeof order.totalBaseAmount === 'string' 
      ? parseFloat(order.totalBaseAmount) 
      : order.totalBaseAmount || 0
    return sum + (isNaN(amount) ? 0 : amount)
  }, 0)
  
  const stats = {
    totalOrders: orders.length,
    totalAmount: totalAmount
  }
  
  // Format order data for display
  const formattedOrders = orders.map(order => ({
    orderId: order.orderId || order.id || 'N/A',
    totalBaseAmount: order.totalBaseAmount || 0,
    status: order.status || 'N/A',
    createTime: order.createTime || order.createdAt || 'N/A',
    updateTime: order.updateTime || order.updatedAt || 'N/A',
    currency: order.currency || 'N/A',
    paymentMethod: order.paymentMethod || 'N/A',
    buyerId: order.buyerId || 'N/A',
    sellerId: order.sellerId || 'N/A'
  }))
  
  return {
    orders: formattedOrders,
    stats: stats
  }
}

/**
 * Prepares data for Excel export
 * @param {Array} orders - Array of formatted order objects
 * @param {Object} stats - Statistics object
 * @returns {Array} Array ready for Excel export with summary row
 */
export function prepareExcelData(orders, stats) {
  // Create a copy of orders and add summary row
  const dataWithSummary = [...orders]
  
  // Add a summary row at the end
  dataWithSummary.push({
    orderId: 'TOTAL',
    totalBaseAmount: stats.totalAmount,
    status: '',
    createTime: '',
    updateTime: '',
    currency: '',
    paymentMethod: '',
    buyerId: '',
    sellerId: ''
  })
  
  return dataWithSummary
}
