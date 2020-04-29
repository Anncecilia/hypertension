// MarkPaperList.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>已标注文献检索</el-breadcrumb-item>
                <router-link :to="{name: 'AllPaper'}">
                    <div class="back-btn">
                        <el-button round size="mini">返回</el-button>
                    </div>
                </router-link> 
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <div class="search">
            <el-row>
                <!-- <el-col :span="8"> -->
                <el-input class="input_bar" v-model="search_key" size="medium" placeholder="请输入检索关键词" clearable></el-input>
                <!-- </el-col> -->
                
                <el-button type="primary" size="medium" @click="Search()" >检索</el-button>
            </el-row>
        </div>
        <el-divider></el-divider>
        <div class="high_search">
            <el-form label-width="80px" :model="form" label-position="left" class="form_bar">
                <el-form-item label="作者：">
                  <el-input v-model="author" class="input_bar"></el-input>
                </el-form-item>
                <el-form-item label="标题：">
                    <el-input v-model="title" class="input_bar"></el-input>
                </el-form-item>
                <el-form-item label="关键词：">
                    <el-input v-model="key" class="input_bar"></el-input>
                </el-form-item>
                <el-form-item label="知识库：">
                    <el-select v-model="select_src" clearable placeholder="请选择">
                        <el-option
                             v-for="item in options_src"
                            :key="item.value"
                            :label="item.label"
                            :value="item.label"> 
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <el-button type="primary" size="medium" @click="HighSearch()" >检索</el-button>
            <el-button type="primary" size="medium" plain>重置</el-button>
        </div>
        <el-divider></el-divider>
        <div class='paper_table' align="center">
            <h2>
                检索结果列表
            </h2>
            <el-table 
                :data="tableData" max-height="400" border style="width:75%">
                <el-table-column type="index" :index=1 label="编号" width="80" align="center"></el-table-column>
                <el-table-column prop="title" label="文献标题" width="600" align="center"></el-table-column>
                <el-table-column prop="author" label="作者" align="center"></el-table-column>
                <el-table-column prop="src" label="来源数据库" align="center"></el-table-column>
                <el-table-column label="操作" width="100" align="center">
                    <template slot-scope="scope">
                      <el-button type="primary" plain size="mini"
                        @click="handleEdit(scope.$index, scope.row)">查看</el-button>
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
    
            //检索
            search_key:"",

            //高级检索
            author:"",
            title:"",
            key:"",
    
            /* mogodb搜索框 */
            searchTable:"",
            searchMsg:"",
    
            tableData:[],
            data_array:[],

            //知识库
            options_src:[{
                value: '1',
                label: '万方数据知识服务平台'
            },{
                value: '2',
                label: '中国知识资源总库（CNKI）'
            },{
                value: '3',
                label: '中国医学科学院医学信息研究所文献平台(UnionSearch)'
            },{
                value: '4',
                label: '美国生物医学文献数据库（PubMed）'
            }],
            select_src:"",
        }
    },
    
    methods: {
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
    
        getPaperList(msg) {
            const path = `http://localhost:5000/search/paper/mark/list`
    
            axios
            .get(path,{
                params:{
                    info:msg,
                }
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
        Search(){
            let msg = {
                type: 'common',
                search_key: this.search_key
            }
            this.getPaperList(msg)
        },
        HighSearch(){
            let msg = {
                type: 'advanced',
                author: this.author,
                title: this.title,
                key: this.key,
                src: this.select_src
            }
            this.getPaperList(msg)
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
        let msg = {
            type: 'start'
        }
        this.getPaperList(msg);
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
        margin-bottom:5%;
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
    .search{
        margin-top: 3%;
    }
    .high_search{
        margin-top: 3%;
        /* width: 32%; */
        margin-left:33%;
        margin-right:33%;
    }
    .input_bar{
        /* margin-left: 10%; */
        width: 400px;
    }
    .el-select{
        width: 400px;
    }
    .el-divider{
        margin-left: 10%;
        margin-right: 10%;
        width: 80%;
    }
    </style>
    