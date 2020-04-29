// Update.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>知识图谱更新</el-breadcrumb-item>
                <router-link :to="{name: 'Home'}">
                    <div class="back-btn">
                        <el-button round size="mini">返回</el-button>
                    </div>
                </router-link> 
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <div v-if="is_update" id="update_msg">
            <h2>
                所有文献都已提交审核!
            </h2>
        </div>
        <div class='paper_table' align="center" v-else>
            <h2>
                待审核文献列表
            </h2>
            <el-table 
                :data="tableData" max-height="400" border style="width:75%">
                <el-table-column type="index" :index=1 label="编号" width="80" align="center"></el-table-column>
                <el-table-column prop="mark_user" label="标注人" width="150" align="center"></el-table-column>
                <el-table-column prop="title" label="文献标题" align="center"></el-table-column>
                <el-table-column label="操作" width="150" align="center">
                    <template slot-scope="scope">
                      <el-button type="primary" plain size="mini"
                        @click="handleEdit(scope.$index, scope.row)">查看标注内容</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="submit_btn">
                <el-button type="primary" size="medium" @click="submit()">一键提交</el-button>
            </div>
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
    
            tableData:[],
            data_array:[],

            //所有文献是否都已提交更新
            is_update:true,
        }
    },
    
    methods: {
        returnHome() {
            this.$router.push({
                path: '/home', 
                name:"Home",
            })
        },
        submit(){
            const path = `http://localhost:5000/submit/update`
    
            axios
            .get(path)
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    alert(this.result.msg)
                    //路由跳转
                    this.returnHome()
                }
                else{
                    alert(this.result.msg)
                }    
            })
            .catch(error => {
                console.log(error)
            })
        },
        sendPaper(paper_id) {
            this.$router.push({
                path: '/paper/mark/detail', 
                name:"MarkPaperDetail",
                params: { 
                    id: paper_id, 
                    data: this.data_array
                },
            })
        },
        handleEdit(index, row) {
            //console.log(index);
            //console.log(row);
            console.log(this.data_array[index].id)
            let id = this.data_array[index].id
            this.sendPaper(id)
        },
    
        getPaperList() {
            const path = `http://localhost:5000//search/paper/update`
    
            axios
            .get(path,{
            })
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    /* alert(this.result.msg) */
                    if(this.result.msg === '查询成功!'){
                        this.tableData = response.data.data
                        this.data_array = JSON.parse(JSON.stringify(this.result.data))
                        this.is_update = false
                    }
                    else{
                        this.is_update = true
                    }  
                }
                else{
                    alert("ERROR")
                }    
            })
            .catch(error => {
                console.log(error)
            })
        },
    },

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
    .submit_btn{
        margin-top: 3%;
    }
    #update_msg{
        margin-top: 10%;
    }
    </style>
    