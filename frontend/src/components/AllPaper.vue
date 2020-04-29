// AllPaper.vue

<template>

    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <router-link :to="{name: 'Home'}">
                    <el-button round size="mini" class="back-btn">返回</el-button>
                </router-link>
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <el-row>
            <router-link :to="{name: 'MarkPaperList'}">
                <el-button type="primary" class="firstpage_btn" plain @click="">已标注文献检索</el-button>
            </router-link>
            <router-link :to="{name: 'UnmarkPaperList'}">
                <el-button type="primary" class="firstpage_btn" plain @click="">查看未标注文献</el-button>
            </router-link>
            <router-link :to="{name: 'PdfList'}">
                <el-button type="primary" class="firstpage_btn" plain @click="">完整文献预览及上传</el-button>
            </router-link>
        </el-row>

        <div id="header">
            <img src="../assets/hypertension.png">
        </div>
    </div>

</template>

<script type="text/javascript">

import axios from 'axios'

export default {

data () {

    return {
        result: "",
        result_mongo:"",

        /* neo4j搜索框 */
        disease_input:"",
        searchVal:"",
        searchData:"",
        now:-1,
        //test
        products:[
            {name:"1",class:"1",id:"1"},
            {name:"2",class:"2",id:"2"},
            {name:"2",class:"2",id:"2"}
        ],

        /* mogodb搜索框 */
        searchTable:"",
        searchMsg:"",

        tabletype:'',
    }
},

methods: {

    getNodeInfo (search) {
        const path = `http://localhost:5000/graph/create`

        axios
        .get(path,{
            params:{
                key: search
            }
        })
        .then(response => {
            this.result = response.data
        })
        .catch(error => {
            console.log(error)
        })

    },

    getGraph (search) {
        this.result = this.getNodeInfo(search)
    },

    getMongo(search_table, search_msg) {
        const path = `http://localhost:5000/mongo/query`

        axios
        .get(path,{
            params:{
                table: search_table,
                msg: search_msg
            }
        })
        .then(response => {
            this.result_mongo = response.data
        })
        .catch(error => {
            console.log(error)
        })
    },



},


}

</script>

<style type="text/css" scoped>

.breadcrumb{
    margin-left:10%;
    width: 80%;
    height:50px;
}
.bc{
    margin-left:20px;
    padding-top:20px;
    
}

#bar{
    height: 20px;
    width: 100%;
    background-color:#e5e5e5;
}
.back-btn{
    margin-left:80%;
    margin-top:-2%;
}
.firstpage_btn{
    height:60px;
    margin:3% 5%;
}
</style>
