// UnmarkPaperList.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>查看未标注文献</el-breadcrumb-item>
                <router-link :to="{name: 'AllPaper'}">
                    <div class="back-btn">
                        <el-button round size="mini">返回</el-button>
                    </div>
                </router-link> 
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <div class='paper_table' align="center">
            <h2>
                未标注文献列表
            </h2>
            <el-table 
                :data="tableData" max-height="400" border style="width:75%">
                <el-table-column type="index" :index=1 label="编号" width="80" align="center"></el-table-column>
                <el-table-column prop="title" label="文献标题" width="750" align="center"></el-table-column>
                <el-table-column prop="src" label="来源数据库" align="center"></el-table-column>
                <el-table-column label="操作" width="120" align="center">
                    <template slot-scope="scope">
                      <el-button type="primary" plain size="mini"
                        @click="handleEdit(scope.$index, scope.row)">开始标注</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!-- <p>
                {{ message }}
            </p> -->
        </div>
    </div>

</template>

<script type="text/javascript">

    import axios from 'axios'
    
    export default {
    
    data () {
    
        return {
            result: "",
            message:"",
    
            /* neo4j搜索框 */
            disease_input:"",
            searchVal:"",
            searchData:"",
            now:-1,
    
            /* mogodb搜索框 */
            searchTable:"",
            searchMsg:"",
    
            tableData:[],
            data_array:[],
        }
    },
    
    methods: {
        sendPaper(paper_id,paper_index) {
            this.$router.push({
                path: '/paper/unmark/detail', 
                name:"PaperDetail",
                params: { 
                    id: paper_id, 
                    index: paper_index,
                    data: this.data_array
                },
            })
        },
        handleEdit(index, row) {
            //console.log(index);
            //console.log(row);
            console.log(this.data_array[index].id)
            let id = this.data_array[index].id
            this.sendPaper(id,index)
        },
    
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
    
        getPaperList() {
            const path = `http://localhost:5000/search/paper/unmark/list`
    
            axios
            .get(path,{
            })
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    this.tableData = response.data.data
                    this.data_array = JSON.parse(JSON.stringify(this.result.data))
                }
                else{
                    alert(this.result.msg)
                }    
            })
            .catch(error => {
                console.log(error)
            })
        },
    },

    /* watch: {
        // 监测路由变化,只要变化了就调用获取路由参数方法将数据存储本组件即可
        //'$route': 'getParams',
        '$route.path':function(newVal,oldVal){
            console.log(newVal+"---"+oldVal);
            if(newVal === '/paper/unmark/list'){
                this.getPaperList();
                this.message = "aaa";
            } 
        }
    }, */
    created: function () {
        this.getPaperList();
    },
    
    
    };
    
    </script>
    
    <style type="text/css" scoped>
    
    .breadcrumb{
        margin-left:10%;
        width: 80%;
        height:50px;
    }
    .bc{
        margin-left:20px;
        /* padding-top:20px; */
        height:50px;
        line-height: 50px;
    }
    
    #bar{
        height: 20px;
        width: 100%;
        background-color:#e5e5e5;
    }
    .back-btn{
        float:right;
        display:block;
        margin:0 auto
    }
    .firstpage_btn{
        height:60px;
        margin:3% 5%;
    }
    .paper_table{
        font-size:20px; 
        margin-top:2%;  
    }
    .source-manage{
        font-size:28px;
        text-align:left;
        width:80%;
        margin-left:10%;
        margin-top:5%;
    }
    .paper_table h2{
        text-align: left;
        margin-left: 12%;
    }
    </style>
    