import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  root: '..', // 设置根目录为项目根目录
  server: {
    port: 3000,
    open: true
  },
  build: {
    rollupOptions: {
      input: {
        main: '../index.html',
      }
    }
  },
  optimizeDeps: {
    include: ['vue', 'element-plus', 'xlsx', '@element-plus/icons-vue']
  }
})
