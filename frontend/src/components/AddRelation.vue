<template>
    <div>
        <div class="rel_title">
            <h1>创建关系</h1>
            
        </div> 
        <div class="rel_msg">
            <div class="rel_label">
                <el-select v-model="value" clearable placeholder="请选择想要添加的关系类型" size="medium" style="width:100%">
                    <el-option v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div class="rel_input">
                <div v-if="value==='1'">
                    <p><span>源节点：疾病名称</span><input v-model="disease_i" placeholder="请输入疾病名称"></p>
                    <p>
                        <span>关系：请选择适应证类型</span>
                        <el-select v-model="select_ind" clearable placeholder="请选择适应证类型" size="medium">
                            <el-option v-for="item in options_indication"
                                :key="item.value_indication"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                    </p>
                    <p><span>请输入证据来源</span><input v-model="evi_in_d" placeholder="请输入证据来源"></p>
                    <p><span>目标节点：药品分类</span><input v-model="drug_type_d" placeholder="请输入药品分类"></p>
                </div>
                <div v-if="value==='2'">
                    <p><span>源节点：人群</span><input v-model="people" placeholder="请输入人群"></p>
                    <p>
                        <span>关系：请选择适应证类型</span>
                        <el-select v-model="select_ind_p" clearable placeholder="请选择适应证类型" size="medium">
                            <el-option v-for="item in options_indication"
                                :key="item.value_indication"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                    </p>
                    <p><span>请输入证据来源</span><input v-model="evi_in_p" placeholder="请输入证据来源"></p>
                    <p><span>目标节点：药品分类</span><input v-model="drug_type_p" placeholder="请输入药品分类"></p>
                </div>
                <div v-if="value==='3'">
                    <p><span>源节点：疾病名称</span><input v-model="disease_c" placeholder="请输入疾病名称"></p>
                    <p>
                        <span>关系：请选择禁忌证类型</span>
                        <el-select v-model="select_c" clearable placeholder="请选择禁忌证类型" size="medium">
                            <el-option v-for="item in options_contraindication"
                                :key="item.value_contraindication"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                    </p>
                    <p><span>请输入证据来源</span><input v-model="evi_con" placeholder="请输入证据来源"></p>
                    <p><span>目标节点：药品分类</span><input v-model="drug_type_c" placeholder="请输入药品分类"></p>
                </div>
                <div v-if="value==='4'">
                    <p><span>源节点：药品分类</span><input v-model="drug_type_in1" placeholder="请输入药品分类"></p>
                    <p>
                        <span>关系：请选择药物相互作用</span>
                        <el-select v-model="select_int" clearable placeholder="请选择药物相互作用" size="medium">
                            <el-option v-for="item in options_interaction"
                                :key="item.value_interaction"
                                :label="item.label"
                                :value="item.label">
                            </el-option>
                        </el-select>
                    </p>
                    <p><span>请输入证据来源</span><input v-model="evi_interaction" placeholder="请输入证据来源"></p>
                    <p><span>目标节点：药品分类</span><input v-model="drug_type_in2" placeholder="请输入药品分类"></p>
                </div>
                <div v-if="value==='5'">
                    <p><span>源节点：药品分类</span><input v-model="drug_type_drug" placeholder="请输入药品分类"></p>
                    <p><span>关系：分类等级</span><input v-model="level_drug" placeholder="请输入分类等级（一级/二级等）"></p>
                    <p><span>请输入证据来源</span><input v-model="evi_level1" placeholder="请输入证据来源"></p>
                    <p><span>目标节点：药品名称</span><input v-model="drug_name" placeholder="请输入药品名称"></p>
                </div>
                <div v-if="value==='6'">
                    <p><span>源节点：药品分类</span><input v-model="drug_type_type1" placeholder="请输入药品分类"></p>
                    <p><span>关系：分类等级</span><input v-model="level_type" placeholder="请输入分类等级（一级/二级等）"></p>
                    <p><span>请输入证据来源</span><input v-model="evi_level2" placeholder="请输入证据来源"></p>
                    <p><span>目标节点：药品分类</span><input v-model="drug_type_type2" placeholder="请输入药品分类"></p>
                </div>
                
            </div>
            <el-button type="primary" size="medium" @click="AddRelation()" class="rel_inform_btn">确定</el-button>           
            <p>{{ test }}</p>
        </div>
    </div>
</template>

<script type="text/javascript">

import axios from 'axios'

export default {
    //注册组件
    data(){
       return{
            test: '',

            //疾病-适应证-药品分类
            disease_i:'',           //疾病
            evi_in_d:'',            //适应证证据来源
            drug_type_d:'',         //药品分类
            select_ind:'',          //选择的适应证分类

            //人群-适应证-药品分类
            people:'',              //人群
            evi_in_p:'',            //适应证证据来源
            drug_type_p:'',         //药品分类
            select_ind_p:'',        //选择的适应证分类

            //疾病-禁忌证-药品分类
            disease_c:'',           //疾病
            evi_con:'',             //禁忌证证据来源
            drug_type_c:'',         //药品分类
            select_c:'',            //选择的药品分类

            //药品分类-药物相互作用-药品分类
            drug_type_in1:'',       //药品分类（源节点）
            evi_interaction:'',     //相互作用证据来源
            drug_type_in2:'',       //药品分类（目标节点）
            select_int:'',            //选择的药品分类

            //药品分类-分类-药品
            drug_type_drug:'',      //药品分类
            level_drug:'',          //分类等级
            evi_level1:'',          //分类证据来源
            drug_name:'',           //药品

            //药品分类-分类-药品分类
            drug_type_type1:'',     //药品分类（源节点）
            level_type:'',          //分类等级
            evi_level2:'',          //分类证据来源
            drug_type_type2:'',     //药品分类（目标节点）
  
            options:[{
                value: '1',
                label: '疾病-适应证->药品分类'
            },{
                value: '2',
                label: '人群-适应证->药品分类'
            },{
                value: '3',
                label: '疾病-相对/绝对禁忌证->药品分类'
            },{
                value: '4',
                label: '药品分类-药物相互作用->药品分类'
            },{
                value: '5',
                label: '药品分类-分类->药品'
            },{
                value: '6',
                label: '药品分类-分类->药品分类'
            }],

            options_indication:[{
                value_indication: '1',
                label: '+（适应）'
            },{
                value_indication: '2',
                label: '-（不适应）'
            },{
                value_indication: '3',
                label: '±（可能适应）'
            }],

            options_contraindication:[{
                value_contraindication: '1',
                label: '相对'
            },{
                value_contraindication: '2',
                label: '绝对'
            }],

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
            value:'',         
       }      
    },

    methods:{
        AddRelation(){
            var start_name = ''
            var start_label = ''
            var end_name = ''
            var end_label = ''
            var relation_name = ''
            var relation_attr = ''
            //疾病-适应证->药品分类
            if(this.value === '1'){
                start_name = this.disease_i
                start_label = "疾病"
                end_name = this.drug_type_d
                end_label = "药品类型"
                relation_name = "适应证"
                relation_attr = {
                    'type': this.select_ind,
                    'evidence': this.evi_in_d
                }    
            }
            //人群-适应证->药品分类
            else if(this.value === '2'){
                start_name = this.people
                start_label = "人群"
                end_name = this.drug_type_p
                end_label = "药品类型"
                relation_name = "适应证"
                relation_attr = {
                    'type': this.select_ind_p,
                    'evidence': this.evi_in_p
                }
            }
            //疾病-相对/绝对禁忌证->药品分类
            else if(this.value === '3'){
                start_name = this.disease_c
                start_label = "疾病"
                end_name = this.drug_type_c
                end_label = "药品类型"
                relation_name = "禁忌证"
                relation_attr = {
                    'type': this.select_c,
                    'evidence': this.evi_con
                }
            }
            //药品分类-药物相互作用->药品分类
            else if(this.value === '4'){
                start_name = this.drug_type_in1
                start_label = "药品类型"
                end_name = this.drug_type_in2
                end_label = "药品类型"
                relation_name = "药物相互作用"
                relation_attr = {
                    'type': this.select_int,
                    'evidence': this.evi_interaction
                }
            }
            //药品分类-分类->药品
            else if(this.value === '5'){
                start_name = this.drug_type_drug
                start_label = "药品类型"
                end_name = this.drug_name
                end_label = "药品"
                relation_name = "分类"
                relation_attr = {
                    'type': this.level_drug,
                    'evidence': this.evi_level1
                }
            }
            //药品分类-分类->药品分类
            else if(this.value === '6'){
                start_name = this.drug_type_type1
                start_label = "药品类型"
                end_name = this.drug_type_type2
                end_label = "药品类型"
                relation_name = "分类"
                relation_attr = {
                    'type': this.level_type,
                    'evidence': this.evi_level2
                }
            }
            else{
                alert("ERROR")
            }

            const path = `http://localhost:5000/graph/create/relation`

            var start = {
                'name': start_name,
                'type': start_label,
                'attr': ''
            }
            var end = {
                'name': end_name,
                'type': end_label,
                'attr': ''
            }
            var relation = {
                'name': relation_name,
                'attr': relation_attr
            }

            this.test = {
                'start': start,
                'end': end,
                'relation': relation
            }

            axios
            .get(path,{
                params:{
                    'start_node': start,
                    'end_node': end,
                    'relation': relation
                }
            })
            .then(response => {
                var is_success = response.data.code
                if(is_success == 200){
                    alert("插入关系成功")
                }
                else{
                    alert(response.data.msg)
                }
                
            })
            .catch(error => {
                console.log(error)
            })
        }
        
    }
}



</script>

<style type="text/css">

.rel_msg{
    
    width:100%;
    
}


.rel_label{
    width:20%;
    float: center;
    margin-top:5%;
    margin-left:40%;
}

.rel_input{
    width:100%;
    margin-top:2%;
    float:center;
    
}

.rel_input p{
    margin-top:40px;
}

.rel_input input{
    width:250px;
    height:30px;
    padding-left:10px;
    margin-left:20px;
    font-size:16px;
}

.rel_inform_btn{
    margin-top:50px;
}



</style>

