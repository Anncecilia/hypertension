// PaperDetail.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>查看未标注文献</el-breadcrumb-item>
                <el-breadcrumb-item>标注文献</el-breadcrumb-item>
                <router-link :to="{name: 'UnmarkPaperList'}">
                    <div class="back-btn">
                        <el-button round size="mini">返回</el-button>
                    </div>
                </router-link> 
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
            <h3>标注内容</h3>
            <el-divider></el-divider>
            <div class="grapy_type">
                <h4>所属子图类型</h4>
                <div class="sub_box">
                    <el-select v-model="graph_value" clearable placeholder="请选择">
                        <el-option
                             v-for="item in graph_type"
                            :key="item.value"
                            :label="item.label"
                            :value="item.label"> 
                        </el-option>
                    </el-select>
                </div>  
            </div>
            <el-divider></el-divider>
            <div class="relation">
                <h4>提取关系</h4>
                <div class="shiyingzheng" v-if = "graph_value==='适应证'">
                    <div class="sub_box">
                        <div class="sub_title">药品名称:</div>
                        <el-input v-model="end_name" placeholder="请输入药品名称" type="text" size="medium" clearable></el-input>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">用药目的:</div>
                        <el-select v-model="select_aim" clearable placeholder="请选择用药目的" size="medium">
                            <el-option v-for="item in drug_aim"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">适用人群:</div>
                        <el-select v-model="select_people" clearable placeholder="请选择适用人群" size="medium">
                            <el-option v-for="item in people"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">关系</div>
                        <el-select v-model="relation_type" :disabled="is_type" placeholder="请选择"></el-select>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">关系属性:</div>
                        <el-select v-model="select_rel" clearable placeholder="请选择适应证类型" size="medium">
                            <el-option v-for="item in options_indication"
                                :key="item.value_indication"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">疾病/症状:</div>
                        <el-input v-model="start_name" placeholder="请输入疾病/症状" type="text" size="medium" clearable></el-input>
                    </div>
                </div> 
                <div class="jinji" v-if = "graph_value==='禁忌证'">
                    <div class="sub_box">
                        <div class="sub_title">源节点</div>
                        <el-select v-model="select_start" clearable placeholder="请选择源节点类型">
                            <el-option
                                v-for="item in node_type"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                        <div class="sub_select" v-if = "select_start">
                            <div class="sub_title">节点名称</div>
                            <el-input v-model="start_name" placeholder="请输入源节点名称" type="text" size="medium" clearable></el-input>
                        </div>
                    </div>
                    <div class="sub_box">
                        <div>
                            <div class="sub_title">关系</div>
                            <el-select v-model="relation_type" :disabled="is_type" placeholder="请选择"></el-select>
                        </div>
                        <div class="sub_select" v-if = "graph_value">
                            <div class="sub_title">关系属性</div>
                            
                            <el-select v-model="select_rel" clearable placeholder="请选择禁忌证类型" size="medium">
                                <el-option v-for="item in options_contraindication"
                                    :key="item.value_contraindication"
                                    :label="item.label"
                                    :value="item.label">
                                </el-option>
                            </el-select>
                            
                        </div>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">目标节点</div>
                        <el-select v-model="select_end" clearable placeholder="请选择目标节点">
                            <el-option
                                v-for="item in node_type"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                        <div class="sub_select" v-if = "select_end">
                            <div class="sub_title">节点名称</div>
                            <el-input v-model="end_name" placeholder="请输入目标节点名称" type="text" size="medium" clearable></el-input>
                        </div>
                    </div>     
                </div> 
                <div class="shiyingzheng" v-if = "graph_value==='药品相互作用'">
                    <div class="sub_box">
                        <div class="sub_title">药品1名称:</div>
                        <el-input v-model="start_name" placeholder="请输入药品1名称" type="text" size="medium" clearable></el-input>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">药品2名称:</div>
                        <el-input v-model="end_name" placeholder="请输入药品2名称" type="text" size="medium" clearable></el-input>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">关系</div>
                        <el-select v-model="relation_type" :disabled="is_type" placeholder="请选择"></el-select>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">临床建议:</div>
                        <el-select v-model="select_rel" clearable placeholder="请选择临床建议" size="medium">
                            <el-option v-for="item in recommend"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="sub_box">
                        <div class="sub_title">作用机制:</div>
                        <el-input v-model="mechanism" placeholder="请输入作用机制" type="text" size="medium" clearable></el-input>
                    </div>
                </div>       
            </div>
            <el-divider></el-divider>
            <div class="evi_level">
                <h4>证据级别</h4>
                <div class="sub_box">
                    <!-- <el-select v-model="evi_value" clearable placeholder="请选择">
                        <el-option
                             v-for="item in evi_level"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"> 
                        </el-option>
                    </el-select> -->
                    <el-input v-model="evi_value" placeholder="请输入证据级别" type="text" size="medium" clearable></el-input>
                </div>
            </div> 
            <el-divider></el-divider>
            <div class="evi_msg">
                <h4>证据依据</h4>
                <div class="sub_box">
                    <el-input v-model="evi_info" placeholder="请输入临床依据" type="text" size="medium" clearable></el-input>
                </div>
            </div>
            
        </div>
        <div class="check_btn">
           <!--  <el-button type="primary" size="medium" @click="AddRelation()" >确定</el-button> -->
           <el-button type="primary" size="medium" @click="Invalid()" plain>不合格</el-button>
           <el-button type="primary" size="medium" @click="Confirm()" >确定并提交</el-button>
           <el-button type="primary" size="medium" @click="Next()" plain>下一篇</el-button>
           
        </div>
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
    
            tableData:[],
            data_dict:{},

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
            }, {
                value: 'others',
                label: '其他'
            }],
            evi_value:'',

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

            node_type:[{
                value: '1',
                label: '疾病'
            }, {
                value: '2',
                label: '人群'
            }, {
                value: '3',
                label: '药品分类'
            }, {
                value: '4',
                label: '药品'
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

            //属性选择
            select_rel:'',
            select_start:'',
            select_end:'',  
            select_aim:'',
            select_people:'',

            //节点名
            start_name:'',
            end_name:'',

            evi_info:"",

            /* 适应证 */
            //用药目的
            drug_aim:[{
                value: '治疗用药',
                label: '治疗用药：是指一切以解除病痛为核心的用药目的，包括一般意义上的治疗、对症治疗和姑息治疗等'
            },{
                value: '辅助治疗用药',
                label: '辅助治疗用药：是指药品在治疗行为过程中起辅助作用，包括消毒用药、康复用药、恶性肿瘤辅助用药等'
            },{
                value: '预防用药',
                label: '预防用药：是指药品用于预防某种疾病的发生，如疫苗接种、健康危险因素预防等'
            },{
                value: '诊断用药',
                label: '诊断用药：是指药品用于某种疾病的诊断过程当中，包括直接诊断、辅助诊断等'
            },{
                value: '操作用药',
                label: '操作用药：是指药品用于某项临床操作过程中，如手术用药、检查用药、麻醉用药等'
            }],
            //人群
            people:[{
                value: '新生儿',
                label: '新生儿：指出生28天以内的人群'
            },{
                value: '婴儿',
                label: '婴儿：指1岁以内的人群'
            },{
                value: '幼儿',
                label: '幼儿：指1岁至3岁之间的人群'
            },{
                value: '儿童',
                label: '儿童：指14岁以下的人群'
            },{
                value: '青少年',
                label: '青少年：指14岁至18岁之间的人群'
            },{
                value: '青年',
                label: '青年：指14岁至35岁之间的人群'
            },{
                value: '育龄女性',
                label: '育龄女性：指15岁至49岁之间的女性人群'
            },{
                value: '中老年人',
                label: '中老年人：指45岁以上人群'
            },{
                value: '老年人',
                label: '老年人：指60岁以上人群'
            }],
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

            /* 药品相互作用 */
            //临床建议
            recommend:[{
                value: 'A',
                label: '避免合用（aviod，A）'
            },{
                value: 'P',
                label: '谨慎合用（precaution，P）'
            },{
                value: 'C',
                label: '可以合用（coadministration，C）'
            },],
            mechanism:'',
        }
    },
    
    methods: {
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
            delete this.result.data["title"];
            delete this.result.data["_id"];
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
        SendMarkParams(params){
            const path = `http://localhost:5000/search/paper/save`
    
            axios
            .get(path,{
                params
            })
            .then(response => {   
                this.result = response.data
                alert(this.result.msg)
            })
            .catch(error => {
                console.log(error)
            })
        },
        Submit(){
            /* console.log(this.graph_value, this.evi_value)
            console.log(this.select_rel) */
            let params = ''
            if (this.relation_type == "适应证"){
                params = {
                    id: this.paper_id,
                    start_name: "疾病",
                    start_type: this.start_name,
                    end_name: "药品",
                    end_type: this.end_name,
                    rel_name: this.relation_type,
                    rel_attr: this.select_rel,
                    drug_aim: this.select_aim,
                    population: this.select_people,
                    evi_level: this.evi_value,
                    evi_info: this.evi_info,
                    mark_user: this.Common.username
                }
            }
            else if(this.relation_type == "禁忌证"){
                params = {
                    id: this.paper_id,
                    start_name: this.start_name,
                    start_type: this.select_start,
                    end_name: this.end_name,
                    end_type: this.select_end,
                    rel_name: this.relation_type,
                    rel_attr: this.select_rel,
                    evi_level: this.evi_value,
                    evi_info: this.evi_info,
                    mark_user: this.Common.username
                }
            }
            else if(this.relation_type == "药品相互作用"){
                params = {
                    id: this.paper_id,
                    start_name: "药品",
                    start_type: this.start_name,
                    end_name: "药品",
                    end_type: this.end_name,
                    rel_name: this.relation_type,
                    rel_attr: this.select_rel,
                    mechanism: this.mechanism,
                    evi_level: this.evi_value,
                    evi_info: this.evi_info,
                    mark_user: this.Common.username
                }
            }
            else{
                console.log("relation_type ERROR")
            }
            console.log(params)
            this.SendMarkParams(params)
        },
        ReturnList() {
            this.$router.push({ 
                path: '/paper/unmark/list', 
                //name:"UnmarkPaperList",
            })
        },
        Confirm(){
            this.Submit()
            //路由跳转
            //alert("跳转")
            //this.ReturnList()
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
        Invalid(){
            const path = `http://localhost:5000/paper/invalid`
            axios
            .get(path,{
                params:{
                    id: this.paper_id,
                }
            })
            .then(response => {
                this.result = response.data 
                alert(this.result.msg) 
                if(this.result.code == 200){
                    //路由跳转
                    this.$router.push({
                        path: '/paper/unmark/list', 
                        name:"UnmarkPaperList",
                    }) 
                }   
            })
            .catch(error => {
                console.log(error)
            })
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
    </style>
    