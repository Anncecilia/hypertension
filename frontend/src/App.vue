<template>
  <div id="app">
    <!-- 导航区域 -->
    <Header/>
    <!-- <img src="./assets/logo.png"> -->
    <router-view/>
  </div>
</template>

<script>
import Header from '@/components/Header'
import UnmarkPaperList from '@/components/UnmarkPaperList'
export default {
  name: 'App',
  components:{
    Header,
  },
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding: 0px 0px;
}
</style>
