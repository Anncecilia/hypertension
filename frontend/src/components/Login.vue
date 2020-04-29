<template>
    
    <div>
        
        <div class="outline">
            <h1>高血压药物研究文献知识管理工具系统</h1>
            <div class="login_header">
				<span @click="cur=0" :class="{active:cur==0}">用户名登录</span>
				<span @click="cur=1" :class="{active:cur==1}">手机号登录</span>
		    </div>
        </div> 

        
        <div class="login" v-show="cur==0">
            <!-- <input type="text" placeholder="用户名" class="id_input" v-model="idVal">
            <span class="search-reset1" @click="clearInput1()">&times;</span>
            <input type="text" placeholder="密码" class="password_input" v-model="passVal">
            <span class="search-reset2" @click="clearInput2()">&times;</span> -->
            <el-input placeholder="请输入用户名" v-model="idVal" class="input_bar"></el-input>
            <el-input placeholder="请输入密码" v-model="passVal" class="input_bar" show-password></el-input>
            <button class="forget_btn" @click="forgetpw()">忘记密码</button>
            <router-link to="/register">
                <button class="register_btn">注册账户</button>
            </router-link>
            <button class="login_btn" @click="login()">登录</button>
                   

        </div>
        
        <div class="login" v-show="cur==1">
            <!-- <input type="text" placeholder="手机号" class="id_input" v-model="phoneVal">
            <span class="search-reset1" @click="clearInput1()">&times;</span>
            <input type="text" placeholder="密码" class="password_input" v-model="passVal">
            <span class="search-reset2" @click="clearInput2()">&times;</span> -->
            <el-input placeholder="请输入手机号" v-model="phoneVal" class="input_bar"></el-input>
            <el-input placeholder="请输入密码" v-model="passVal" class="input_bar" show-password></el-input>
            <button class="forget_btn" @click="forgetpw()">忘记密码</button>
            <router-link to="/register">
                <button class="register_btn">注册账户</button>
            </router-link>
            <button class="login_btn" @click="login()">登录</button>

        </div>

        <!-- <p>{{ result }}</p> -->


    </div>
</template>

<script type="text/javascript">
// import xxx from someSrc     es6中得到模块的方法。

import axios from 'axios'

export default {
    //注册组件
    data(){
       return{
           idVal:"",
           passVal:"",
           phoneVal:"",
           cur:0,
           result: "",
       }
    },

    methods:{
        sendUsername() {
            this.$router.push({
                path: '/home', 
                name:"Home",
                params: { 
                    name: this.idVal, 
                },
            })
        },
        getLogin() {
            const path = `http://localhost:5000/user/login`

            axios
            .get(path,{
                params:{
                    name: this.idVal,
                    password: this.passVal
                }
            })
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    this.sendUsername()
                }
                else{
                    alert(this.result.msg)
                }
                    
            })
            .catch(error => {
                console.log(error)
            })

        },
        clearInput1(){
            this.idVal = "";
        },
        clearInput2(){
            this.passVal = "";
        },

        login(){
            var id = this.idVal;
            var pw = this.passVal;
            var phone = this.phoneVal;
            
            if (id && pw ){
                this.getLogin()
            } 
            else if (phone && pw){     
                this.getLogin()
            }
            else{
                alert('请输入用户名(手机号)或密码')
            }
            
        },

    }
}



</script>

<style type="text/css" scoped>
.login {
    height: 45px;
    width: 420px;
    margin: 0 auto;
    margin-top: 20px;
    border: 1px;
    position: relative;
}

.search-reset1 {
    width: 21px;
    height: 21px;
    position: relative;
    top:-33px;
    left:390px;
    display: block;
    line-height: 21px;
    text-align: center;
    cursor: pointer;
    font-size: 20px;
    
   
}
.search-reset2 {
    width: 21px;
    height: 21px;
    position: relative;
    top:-33px;
    left:390px;
    display: block;
    line-height: 21px;
    text-align: center;
    cursor: pointer;
    font-size: 20px;

   
}

.login_btn {
    
    height: 45px;
    width: 420px;
    border: 1px solid mediumseagreen;
    background-color: mediumseagreen;
    color: white;
    font-size: 16px;
    font-weight: bold;
    float: left;
    margin-top: 10px;
    
}

.forget_btn {
    background-color: transparent;
    border-style: none;
    outline: none;
    color: cornflowerblue;
    
    font-size: 16px;
    float:right;
    margin-top:10px;
}

.register_btn {
    background-color: transparent;
    border-style: none;
    outline: none;
    color: cornflowerblue;
    float:left;
    font-size: 16px;
    margin-top:10px;
}

.login_text {
    font-size:18px;
    
    color: mediumseagreen;
}

.login_header{
    margin-top:50px;
    font-size: 18px;
    
}
.login_header span{
    margin-right: 20px;
    cursor: pointer;
}
.active{
    color: mediumseagreen;
    padding-bottom: 10px;
}
.outline{
    margin-top: 50px;
}
.input_bar{
    margin-bottom: 5%;
}
</style>