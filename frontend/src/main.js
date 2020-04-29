// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
// 引入路由
import router from './router'
import '../static/reset.css'

// 引入echarts,这种方法是直接绑定在vue实例上，所以在项目中任何页面，直接 this.$echarts 即可
// import echarts from 'echarts'
// Vue.prototype.$echarts = echartsnpm i element-ui -S

// elementUI导入
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css' // 注意样式文件需要单独引入

//引入全局变量
import Common from '@/components/Common'
Vue.prototype.Common = Common;

// 调用插件
Vue.use(ElementUI);

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  mode:'history',
  router,
  components: { App },
  template: '<App/>'
})

document.title = '高血压药物研究文献知识管理工具系统'