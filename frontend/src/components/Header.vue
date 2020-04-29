// Header.vue

<template>
        <!-- element-ui -->
        <el-container v-show="$route.meta.navShow">
            <el-header height = '50px' >
                <div class="header">
                    <div class="nav-left">
                        <div class="el-icon-arrow-right" id="sys_name">
                            高血压药物研究文献管理系统&nbsp
                        </div>
                    </div>
                    <div class="nav-left">
                        <div class="el-icon-s-home" id="home">
                            首页
                        </div>
                    </div>
                    <div class="nav-right user" v-if="unlisted">
                        <div id="block_avator"></div>
                        <router-link to="/login">
                            <span>登录</span>
                        </router-link>
                        |  
                        <router-link to="/register">
                            <span>注册</span>
                        </router-link>
                    </div>
                    <div class="nav-right user" v-else>
                        <!-- 用户头像 -->
                        <div id="block_avator"></div>
                        <div class="nav-left">
                            <el-avatar :size="30" :src="circleUrl"></el-avatar>
                        </div>
                        <p class="nav-left">{{ username }}</p>
                    </div>
                    <!-- <p>{{ result }}</p> -->
                </div>
            </el-header>
        </el-container>
</template>
<script>
    export default {
        name: 'Header',
        data(){
            return {
                unlisted: true,
                //unlisted: false,
                username: "Username",
                result:"1",
                circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
            }
        },
        methods: {
            set() {
                this.unlisted = ture
            },
            getParams () {
                // 取到路由带过来的参数 
                let routerParams = this.$route.params.name
                // 将数据放在当前组件的数据内
                this.username = routerParams
                this.Common.username = this.username
                this.unlisted = false
            }
        },
        watch: {
            // 监测路由变化,只要变化了就调用获取路由参数方法将数据存储本组件即可
            //'$route': 'getParams',
            '$route.path':function(newVal,oldVal){
                // console.log(newVal+"---"+oldVal);
                if(newVal === '/home' && oldVal === '/login'){
                    this.getParams();
                } 
            }
        },
    };

</script>

<style type="text/css" scoped>
body {
    margin:0;
    padding:0;
    font-size: 14px;
    color: #4a4a4a;
    /* font-family: PingFangSC-Light; */ /*苹果设计的一款全新的中文系统字体，该字体支持苹果的动态字体调节技术*/
}
.el-header{
    padding: 0px 0px;
}
ul {
    list-style: none;
}
a {
    text-decoration: none;
}
.header{
    background-color:#e5e5e5;
    height: 50px;
}
.nav-left{
    margin-top: 0px;
    margin-bottom: 0px;
    float: left;
}
.nav-right{
    float: right;
}
#sys_name{
    background-color:#16365a;
    color:white;
    font-size: 30px;
    height: 50px;
    line-height: 50px;
}
#home{
    height: 50px;
    text-indent: 10px;
    line-height: 50px;
}
.user{
    height: 50px;
    line-height: 30px;
    margin-right:2%
}
#block_avator{
    height:10px;
}
</style> 