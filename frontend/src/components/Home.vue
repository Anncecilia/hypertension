// Home.vue

<template>

    <div>
        <el-row>
            <router-link to="/paper/all">
                <el-button type="primary" class="firstpage_btn" plain @click="">查看所有文献</el-button>
            </router-link>
            <router-link to="/spider">
                <el-button type="primary" class="firstpage_btn" plain @click="">文献抓取设置</el-button>
            </router-link>
            <router-link to="/update">
                <el-button type="primary" class="firstpage_btn" plain @click="">知识图谱更新</el-button>
            </router-link>
        </el-row>

        <div id="header">
            <img src="../assets/hypertension.png">
        </div>


        <!-- <p>{{ result }}</p>
        <div>
            <p>
                搜索Neo4j
            </p>
        </div>

        <div class="search-input">
            <input type="text" placeholder="请输入疾病名称" class="disease_input" v-model="searchVal">
            <span class="search-reset" @click="clearInput()">&times;</span>
            <button class="search-btn" @click="SearchInfo()">搜索</button>
            <ul v-for="list in searchData">
            	<li>  			
                    <span>{{list.name}}</span>  			
                    <span>{{list.class}}</span>  			
                    <span>{{list.id}}</span>  		
                </li>  	
            </ul>
        </div>

        <div>
            <p>
                搜索MongoDB
            </p>
        </div>
        <div class="search-input">
            <input type="text" placeholder="请输入查询表格" class="disease_input" v-model="searchTable">
            <span class="search-reset" @click="clearInput()">&times;</span>
        </div>

        <div class="search-input">
            <input type="text" placeholder="请输入查询内容" class="disease_input" v-model="searchMsg">
            <span class="search-reset" @click="clearInput()">&times;</span>
        </div>
        <button class="search-btn-mongo" @click="SearchMongoInfo()">搜索</button>
        <div class="all_table">
            <table v-if="tabletype==='search_disease_table'">
                <thead>
                    <tr>
                        <th>疾病名称</th>
                        <th>ICD-11编码或章节码</th>
                        <th>是否为有效码</th>
                        <th>别名</th>
                        <th>英文名</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="list in result_mongo">
                        <td v-text="list.name"></td>
                        <td v-text="list.chapter_or_code"></td>
                        <td v-text="list.valid"></td>
                        <td v-text="list.byname"></td>
                        <td v-text="list.english"></td>
                    </tr>
                </tbody>
            </table>
        </div> -->
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
    /* getRandomFromBack () {
        const path = `http://localhost:5000/api/random`
        axios.get(path)
        .then(response => {
            this.randomNumber = response.data.randomNumber
        })
        .catch(error => {
            console.log(error)
        })
    }, */

    getNodeInfo (search) {
        const path = `http://localhost:5000/graph/create`

        axios
        .get(path,{
            params:{
                key: search
            }
        })
       /*  axios({
            method: 'post',
            url: path,
            data: {'key': "高血压"},
	    }) */
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

    /* 清除输入框内容 */
    clearInput:function () {
        this.searchVal="";
    },

    /* 按下neo4j搜索按钮 */
    SearchInfo () {
        var search = this.searchVal;
        if (search){
            /* this.searchData = this.products.filter(function(product){
                console.log(product)
                return Object.keys(product).some(function(key){
                    console.log(key)
                    return String(product[key]).toLowerCase().indexOf(search) > -1
                })
            }) */
            this.getGraph(search);
        }
    },

    /* 按下mongodb搜索按钮 */
    SearchMongoInfo() {
        var search_table = this.searchTable;
        var search_msg = this.searchMsg;
        if(search_table){
            this.getMongo(search_table, search_msg);
            if(search_table == "disease"){
            this.tabletype = 'search_disease_table';
            }
        }
        
    },

},

created () {

}

}

</script>

<style type="text/css" scoped>
table{
    font-family: verdana,arial,sans-serif;
    font-size:18px;
    color:#333333;
    
    margin:auto;
    border-width: 1px;
    border-color: #666666;
    border-collapse: collapse;
}
th {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #dedede;
}
td,tr {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #ffffff;
}
.search-input {
    height: 45px;
    width: 600px;
    margin: 0 auto;
    margin-top: 10px;
    border: 1px;
    position: relative;
}

.search-input input {
    border: 1px solid #e4e4e4;
    box-sizing: border-box;
    width: 500px;
    height: 45px;
    font-size: 18px;
    float: left;
    padding-left: 10px;
    padding-right: 10px;
    overflow: hidden;
}

.search-btn {
    height: 45px;
    width: 100px;
    border: 1px solid mediumseagreen;
    background-color: mediumseagreen;
    color: white;
    font-size: 16px;
    font-weight: bold;
    float: left;
}

.search-btn {
    cursor: pointer
}

.search-btn-mongo {
    height: 45px;
    width: 100px;
    border: 1px solid mediumseagreen;
    background-color: mediumseagreen;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 10px;
}


.selectback {
    background-color: #eee !important;
    cursor: pointer
}

input::-ms-clear {
    display: none
}

.search-reset {
    width: 21px;
    height: 21px;
    position: absolute;
    display: block;
    line-height: 21px;
    text-align: center;
    cursor: pointer;
    font-size: 20px;
    right: 110px;
    top: 12px
}

.search-select-list {
    transition: all 0.5s
}

.itemfade-enter,
.itemfade-leave-active {
    opacity: 0;
}

.itemfade-leave-active {
    position: absolute;
}

.selectback {
    background-color: #eee !important;
    cursor: pointer
}
.search-select ul{margin:0;text-align: left; }

.firstpage_btn{
    height:60px;
    margin:3% 5%;
}
</style>
