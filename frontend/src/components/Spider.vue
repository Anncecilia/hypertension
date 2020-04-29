<template>
    
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>文献抓取设置</el-breadcrumb-item>
                <router-link :to="{name: 'Home'}">
                    <el-button round size="mini" class="back-btn">返回</el-button>
                </router-link>
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <div class="time-manage">
            <p>抓取设置</p>
            <el-divider></el-divider>
            <div class="set-time">
                <p>
                    <span>是否开启爬虫：</span>
                    <el-switch 
                        v-model="spider_switch" active-color="#13ce66" inactive-color="#ff4949">
                    </el-switch>
                </p>
                <p>
                    <span>选择时间：</span>
                    <el-time-picker arrow-control v-model="timeVal" format="HH:mm" value-format="HH:mm"
                    :picker-options="{selectableRange: '00:00:00 - 23:59:59'}"
                    placeholder="00:00" class='time-select'>
                    </el-time-picker>
                </p>
                <p>
                    <span>选择周期：</span>
                    <!-- <el-input class="input-circle" v-model="circle" size="small" placeholder="请输入抓取周期（单位：天）"></el-input> -->
                    <el-select v-model="circle" class="input-circle" clearable placeholder="请选择抓取周期">
                        <el-option
                            v-for="item in circle_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </p>
                <p>
                    <span>抓取页数设置：</span>
                    <p class="page">起始页：第<el-input class="input-page" v-model="startpage" size="small"></el-input>页&nbsp&nbsp</p>
                    <p class="page">爬取页数：<el-input class="input-page" v-model="page" size="small"></el-input>页</p>
                </p>
            </div>
        </div>

        <div class="source-manage">
            <p>源管理</p>
            <el-divider></el-divider>
            
            <div class='paper_table'>
                <p>中文</p>
                <el-table 
                    ref="multipleTable1"
                    :data="tableData1" heigt="500" border style="width:80%" @selection-change="handleSelectionChange1">
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column prop="id" label="编号" width="100"></el-table-column>
                    <el-table-column prop="name" label="期刊/会议" width="300"></el-table-column>
                    <el-table-column prop="src" label="网址" width="420"></el-table-column>
                </el-table>
                <p>英文</p>
                <el-table 
                    ref="multipleTable2"
                    :data="tableData2" heigt="500" border style="width:80%" @selection-change="handleSelectionChange2">
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column prop="id" label="编号" width="100"></el-table-column>
                    <el-table-column prop="name" label="期刊/会议" width="300"></el-table-column>
                    <el-table-column prop="src" label="网址" width="420"></el-table-column>
                </el-table>

            </div>
        </div>

        <div class="kw-manage">
            <p>关键词管理</p>
            <el-divider></el-divider>
            <div class="select-kw">
                <p>
                    <span>中文关键词已选择：</span>
                    <el-tag
                    :key="tag1" v-for="tag1 in KWTags1"
                    closable
                    :disable-transitions="false"
                    @close="handleClose1(tag1)">{{tag1}}</el-tag>
                    <el-input class="input-new-tag" v-if="inputVisible1" v-model="inputValue1" ref="saveTagInput1" size="small" @keyup.enter.native="handleInputConfirm1" @blur="handleInputConfirm1"></el-input>
                    <el-button v-else class="button-new-tag" size="small" @click="showInput1">+ 添加关键词</el-button>
                </p>
                <p>
                    <span>英文关键词已选择：</span>
                    <el-tag
                    :key="tag2" v-for="tag2 in KWTags2"
                    closable
                    :disable-transitions="false"
                    @close="handleClose2(tag2)">{{tag2}}</el-tag>
                    <el-input class="input-new-tag" v-if="inputVisible2" v-model="inputValue2" ref="saveTagInput" size="small" @keyup.enter.native="handleInputConfirm2" @blur="handleInputConfirm2"></el-input>
                    <el-button v-else class="button-new-tag" size="small" @click="showInput2">+ Add Keywords</el-button>
                </p>
            </div>
        </div>

        <div class="save-btn">
            <el-button type="primary" size="medium" @click="clicksave()">保存</el-button>
        </div>

    </div>
</template>

<script type="text/javascript">

import axios from 'axios'

export default {
    //注册组件
    data(){
       return{
            KWTags1: ['高血压', '随机对照试验', 'ACEI','β受体阻滞剂'],
            KWTags2: ['hypertension', 'RCT','randomized controlled trial', 'ACEI','β-blocker'],
            inputVisible1: false,
            inputVisible2: false,
            inputValue1: '',
            inputValue2: '',

            spider_switch: true,
            timeVal: '',
            startpage: '1',
            page:'',
            circle: '',


            tableData1:[
            /* {
               id:'1',
               name:'中国生物医学文献数据库（CBM）',
               src:'http://www.sinomed.ac.cn/'
            }, */
            {
                id:'1',
                name:'万方数据知识服务平台',
                src:'http://www.wanfangdata.com.cn/index.html'
            },{
                id:'2',
                name:'中国知识资源总库（CNKI）',
                src:'https://www.cnki.net/'
            },{
                id:'3',
                name:'中国医学科学院医学信息研究所文献平台',
                src:'http://www.imicams.ac.cn/'
            }],

            tableData2:[{
                id:'1',
                name:'美国生物医学文献数据库（PubMed）',
                src:'https://pubmed.ncbi.nlm.nih.gov/'
            }],

            circle_options:[{
                value: 'day',
                label: '每日'
            },{
                value: 'week',
                label: '每周'
            },{
                value: 'month',
                label: '每月'
            },{
                value: 'year',
                label: '每年'
            }],



            multipleSelection1: [],
            multipleSelection2: [],


            selectedIDs_c:[],
            selectedIDs_e:[],
            
       }
            
        
    },

    
    

    methods:{


        handleClose1(tag1) {
            this.KWTags1.splice(this.KWTags1.indexOf(tag1), 1);
        },

        showInput1() {
            this.inputVisible1 = true;
            this.$nextTick(_ => {
            this.$refs.saveTagInput1.$refs.input.focus();
            });
        },

        handleInputConfirm1() {
            let inputValue1 = this.inputValue1;
            if (inputValue1) {
                this.KWTags1.push(inputValue1);
            }
            this.inputVisible1 = false;
            this.inputValue1 = '';
        },

        handleClose2(tag2) {
            this.KWTags2.splice(this.KWTags2.indexOf(tag2), 1);
        },

        showInput2() {
            this.inputVisible2 = true;
            this.$nextTick(_ => {
            this.$refs.saveTagInput2.$refs.input.focus();
            });
        },

        handleInputConfirm2() {
            let inputValue2 = this.inputValue2;
            if (inputValue2) {
                this.KWTags2.push(inputValue2);
            }
            this.inputVisible2 = false;
            this.inputValue2 = '';
        },       
        handleSelectionChange1(val) {
            this.multipleSelection1 = val;
            let ids = []
            this.multipleSelection1.map((item)=> {
                ids.push(item.id)
            })
            this.selectedIDs_c = ids
            //console.log(this.selectedIDs_c)
        },
        handleSelectionChange2(val) {
            this.multipleSelection2 = val;
            let ids = []
            this.multipleSelection2.map((item)=> {
                ids.push(item.id)
            })
            this.selectedIDs_e = ids
            //console.log(this.selectedIDs_e)
        },
        
        // 按下保存按钮
        clicksave(){
            /* var msg = {
                "src_c": this.selectedIDs_c,
                "src_e": this.selectedIDs_e,
                "key_c": this.KWTags1,
                "key_e": this.KWTags2,
                "time": this.timeVal,
                "circle": this.circle,
                "start_page": this.startpage,
                "page_num": this.page,
                "spider_switch": this.spider_switch
            }
            console.log(msg) */

            const path = `http://localhost:5000/set/spider`

            axios
            .get(path,{
                params:{
                    src_c: JSON.stringify(this.selectedIDs_c),
                    src_e: JSON.stringify(this.selectedIDs_e),
                    key_c: JSON.stringify(this.KWTags1),
                    key_e: JSON.stringify(this.KWTags2),
                    time: this.timeVal,
                    circle: this.circle,
                    start_page: this.startpage,
                    page_num: this.page,
                    spider_switch: this.spider_switch
                }
            })
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    alert(this.result.msg)
                }
                else{
                    alert(this.result.msg)
                }
                    
            })
            .catch(error => {
                console.log(error)
            })
        },
    }

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

.back-btn{
    margin-left:80%;
    margin-top:-2%;
}

.source-manage{
    font-size:28px;
    text-align:left;
    width:80%;
    margin-left:10%;
    margin-top:5%;
}
.paper_table{
    margin-left:10%;
    margin-top:20px;
    font-size:20px;    
}


.kw-manage{
    font-size:28px;
    text-align:left;
    width:80%;
    margin-left:10%;
    margin-top:5%;
}

.select-kw{
    font-size:16px;
    margin-left:10%;
}

.el-tag + .el-tag {
    margin-left: 10px;
}
.button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
}
.input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
}

.time-manage{
    font-size:28px;
    text-align:left;
    width:80%;
    margin-left:10%;
    margin-top:3%;
}

.set-time{
    font-size:16px;
    margin-left:10%;
}

.input-circle{
    width:220px;
    margin-left:10px;
    margin-right:10px;
}

.save-btn{
    margin-top:100px;
    margin-bottom:100px;
}
.time-select{
    margin-left:10px;
}

.input-page{
    width:60px;
    margin-left:5px;
    margin-right:5px;

}

.page{
    margin-left: 5%;
}

p {
    margin-top: 2%;
}

#bar{
    height: 20px;
    width: 100%;
    background-color:#e5e5e5;
}
</style>

