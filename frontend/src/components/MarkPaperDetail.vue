// PaperDetail.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>已标注文献检索</el-breadcrumb-item>
                <el-breadcrumb-item>查看文献内容</el-breadcrumb-item>
                <!-- <router-link :to="{name: 'MarkPaperList'}"> -->
                <div class="back-btn">
                    <el-button round size="mini" @click="TurnBack()">返回</el-button>
                </div>
                <!-- </router-link>  -->
            </el-breadcrumb>
        </div>
        <div id="bar"></div>

        <h2>{{paper_title}}</h2>
        <ul id="detail_msg">
            <li v-for="(value,key,index) in data_dict">
                <span id="keys">
                    {{ key }}:
                </span>
                <span id="values">
                    {{ value }}
                </span>
            </li>
        </ul>
        <div id="mark">
            <el-divider></el-divider>
            <h3>标注结果</h3>
            <el-divider></el-divider>
            <el-form label-width="150px" :model="form" label-position="left" class="form_bar">
                <!-- <el-form-item class="label" label="源节点类型：">
                    {{ start_type }}
                </el-form-item>
                <el-form-item class="label" label="源节点名称：">
                    {{ start_name }}
                </el-form-item>
                <el-form-item class="label" label="关系类型/所属子图：">
                    {{ rel_name }}
                </el-form-item>
                <el-form-item class="label" label="关系属性：">
                    {{ rel_attr }}
                </el-form-item>
                <el-form-item class="label" label="目标节点类型：">
                    {{ end_type }}
                </el-form-item>
                <el-form-item class="label" label="目标节点名称：">
                    {{ end_name }}
                </el-form-item>
                <el-form-item class="label" label="证据等级：">
                    {{ evi_value }}
                </el-form-item>
                <el-form-item class="label" label="标注人：">
                    {{ mark_user }}
                </el-form-item> -->
                <el-form-item
                    v-for="(value,key,index) in mark_info"
                    :label="key"
                    :key="index"
                > 
                {{ value }}
                </el-form-item>
            </el-form>
        </div>
        <!-- <div class="check_btn">
           <el-button type="primary" size="medium" @click="Next()" plain>下一篇</el-button>          
        </div> -->
    </div>

</template>

<script type="text/javascript">

    import axios from 'axios'
    import Header from '@/components/Header'
    
    export default {
    
    data () {
    
        return {
            result: "",
            message:"",
            mark_key:"",
    
            tableData:[],
            data_dict:{},
            mark_info:{},

            paper_id:'',
            paper_index:'',
            paper_title: '',
            data_array:'',
            next_id:'',
            next_index:'',

            evi_level:[{
                value: 'A',
                label: 'A级 数据来自多项随机对照临床试验或由随机对照临床试验组成的荟萃分析'
            }, {
                value: 'B',
                label: 'B级 数据来自单项随机临床试验或多个大型非随机对照研究'
            }, {
                value: 'C',
                label: 'C级 数据来自专家共识和（或）小规模研究、回顾性研究或登记注册研究'
            }],

            graph_type:[{
                value: '1',
                label: '适应证'
            }, {
                value: '2',
                label: '禁忌证'
            }, {
                value: '3',
                label: '药品相互作用'
            }],
            graph_value:'',
            relation_type:'',
            is_type:false,

            //适应证属性
            options_indication:[{
                value_indication: '1',
                label: 'Ⅰ类 证据和（或）总体一致认为，该治疗或方法有益、有用或有效'
            },{
                value_indication: '21',
                label: 'Ⅱa类 证据/观点倾向于有用/有效'
            },{
                value_indication: '22',
                label: 'Ⅱb类 证据/观点不足以确立有用/有效'
            },{
                value_indication: '3',
                label: 'Ⅲ类 证据和（或）专家一致认为，该治疗或方法无用/无效，在某些情况下可能有害'
            }],
            //禁忌证属性
            options_contraindication:[{
                value_contraindication: '1',
                label: '相对'
            },{
                value_contraindication: '2',
                label: '绝对'
            }],
            //药品相互作用属性
            options_interaction:[{
                value_interaction: '1',
                label: '+（推荐）'
            },{
                value_interaction: '2',
                label: '-（不推荐）'
            },{
                value_interaction: '3',
                label: '±（次要推荐）'
            }],

            value_indication:'',
            value_contraindication:'',
            value_interaction:'', 

            //标注内容
            start_name:'',
            start_type:'',
            end_name:'',
            end_type:'',
            rel_name:'',
            rel_attr:'',
            evi_value:'',
            mark_user:'',
        }
    },
    
    methods: {
        TurnBack(){
            this.$router.go(-1)
        },
        getParams () {
            // 取到路由带过来的参数 
            let routerParams = this.$route.params
            // 将数据放在当前组件的数据内
            this.paper_id = routerParams.id
            this.paper_index = routerParams.index
            this.data_array = routerParams.data
            //console.log(this.paper_id)
        },  
        dataProcess(){
            this.paper_title = this.result.data["title"]
            console.log(this.paper_title)
            /* this.start_name = this.result.data["start_name"]
            this.start_type = this.result.data["start_type"]
            this.end_name = this.result.data["end_name"]
            this.end_type = this.result.data["end_type"]
            this.rel_name = this.result.data["rel_name"] */
            //this.rel_attr = this.result.data["rel_attr"]
           /*  if(this.rel_name == '适应证'){
                this.options_indication.map((item)=>{
                    if(item.value_indication == this.result.data["rel_attr"]){
                        this.rel_attr = item.label
                    }
                })
            }
            else{
                this.rel_attr = this.result.data["rel_attr"]
            }
            
            this.mark_user = this.result.data["mark_user"]
            this.evi_level.map((item)=>{
                if(item.value == this.result.data["evi_level"]){
                    this.evi_value = item.label
                }
            })
            
            delete this.result.data["title"];
            delete this.result.data["_id"];
            delete this.result.data["start_name"];
            delete this.result.data["start_type"];
            delete this.result.data["end_name"];
            delete this.result.data["end_type"];
            delete this.result.data["rel_name"];
            delete this.result.data["rel_attr"];
            delete this.result.data["mark_user"];
            delete this.result.data["evi_level"]; */

            this.mark_info = JSON.parse(JSON.stringify(this.result.data["mark_info"]))
            this.mark_key = Object.keys(this.mark_info)
            delete this.result.data["mark_info"];
            this.data_dict = JSON.parse(JSON.stringify(this.result.data))
            this.message = Object.keys(this.data_dict)
        },
        getPaperDetail() {
            const path = `http://localhost:5000/search/paper/detail`
    
            axios
            .get(path,{
                params:{
                    id: this.paper_id,
                }
            })
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    this.dataProcess()
                }
                else{
                    alert(this.result.msg)
                }    
            })
            .catch(error => {
                console.log(error)
            })
        },
        
        graphChange(){
            console.log("graphchange")
            if(this.graph_value){
                this.relation_type = this.graph_value
                this.is_type = true
                this.select_rel = ''
            }
            else{
                this.relation_type = ''
                this.is_type = false
            }
        },
        Next(){
            this.next_index = this.paper_index + 1
            this.next_id = this.data_array[this.next_index].id
            console.log(this.next_id)
            this.Submit()
            this.paper_id = this.next_id
            this.paper_index = this.next_index
            this.getPaperDetail()
            //清空列表
            this.graph_value = ""
            this.start_name = ""
            this.end_name = ""
            this.select_end = ""
            this.select_rel = ""
            this.select_start = ""
            this.evi_value = ""
        },
    },
    created: function () {
        this.getParams();
        this.getPaperDetail();
    },
    watch: {
        graph_value: 'graphChange'
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

    ul {
        list-style-type: none;
        margin:2% 10%;
        padding: 1% 40px;
        border-style: dashed;
        border-color: #e5e5e5;
    } 

    li{
        margin-top: 1%;
        margin-bottom: 1%;
        text-align: left;
        line-height: 1.5;
    }
    #keys{
        font-size: larger;
        font-weight: bold;
    }
    #values{
        font-size: medium;
        word-wrap: break-word;
        word-break: break-all;
        overflow: hidden
    }
    h2{
        text-align: left;
        margin-left: 8%;
        margin-right: 12%;
        margin-top: 2%;
    }

    #mark{
        margin:2% 10%;
    }

    #mark h3{
        text-align: left;
    }

    h4{
        text-align: left;
    }
    .sub_box{
        text-align: left;
        margin-left: 10%;
        margin-top: 2%;
        margin-bottom: 2%;
    }
    .sub_title{
        float: left;
        width: 10%;
        height: 40px;
        line-height: 40px;
    }
    .check_btn{
        margin: 5% auto;
    }
    .sub_select{
        text-align: left;
        margin-top: 1%;
        margin-bottom: 2%;
    }
    .el-input{
        /* float: left; */
        width: 221.4px;
    }
    .el-form{
        width: 80%;
        margin-left: 5%;
        color: #2c3e50;
        line-height: 40px;
        font-size: medium;
    }
    .el-form-item{
        font-size: large;
        color: #2c3e50;
        text-align: left;
        margin-bottom: 1%;
    }
    .el-form-item__label{
        color: #2c3e50;
        font-size: larger;
    }
    /* .el-form-item label{
        
    } */
    </style>
    