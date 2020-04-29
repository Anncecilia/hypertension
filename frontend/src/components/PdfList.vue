// PdfList.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>文献pdf列表</el-breadcrumb-item>
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
                文献列表
            </h2>
            <div>
                <router-link :to="{name: 'Upload'}">
                    <el-button size="medium" id="upload" type="success" plain>上传本地PDF</el-button>
                </router-link>
            </div>
            <el-table 
                :data="tableData" max-height="400" border style="width:75%">
                <el-table-column type="index" :index=1 label="编号" width="80" align="center"></el-table-column>
                <el-table-column label="文献标题" align="center">
                    <template slot-scope="scope">
                        <span>{{ scope.row }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="130" align="center">
                    <template slot-scope="scope">
                      <el-button type="primary" plain size="mini"
                        @click="handleEdit(scope.$index, scope.row)">预览</el-button>
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
        sendFilename(filename){
            this.$router.push({
                path: '/show/pdf', 
                name:"ShowPdf",
                /* params: { 
                    id: filename, 
                }, */
            })
        },
        handleEdit(index, row) {
            //console.log(index);
            //console.log(row);
            console.log(this.data_array[index].id)
            /* let id = this.data_array[index].id
            this.sendPaper(id,index) */
            let filename = row
            this.sendFilename(filename)
        },
    
        getPaperList() {
            const path = `http://localhost:5000/paper/pdf/list`
    
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
        margin-bottom: 0px;
    }
    #upload{
        /* float: right; */
        position:relative;
        left:33.2%;
        margin-bottom: 5px;
    }
    </style>
    