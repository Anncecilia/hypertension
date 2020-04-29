<template>
    
    <div>
        
        <div class="add_title">
            <h1>添加节点</h1>
            
        </div> 
        <div class="add_msg">
            <div class="add_label">
                <el-select v-model="value" clearable placeholder="请选择想要添加的节点类型" size="medium">
                    <el-option v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div class="add_input">
                <div v-if="value==='1'">
                    疾病名称<input v-model="disease_name" placeholder="请输入疾病名称">
                    <p></p>
                    ICD-11编码<input v-model="disease_icd" placeholder="请输入疾病ICD-11编码">
                </div>
                <div v-if="value==='2'">
                    药品类型<input v-model="drug_type" placeholder="请输入药品类型">
                </div>
                <div v-if="value==='3'">
                    药品名称<input v-model="drug_name" placeholder="请输入药品名称">
                    <p></p>
                    药品ATC编码<input v-model="drug_atc" placeholder="请输入药品ATC编码">
                </div>
                <div v-if="value==='4'">
                    人群<input v-model="people" placeholder="请输入人群">
                </div>
                
            </div>
            <el-button type="primary" size="medium" @click="AddInfo()" class="inform_btn">确定</el-button>           
        </div>
    </div>
</template>

<script type="text/javascript">

import axios from 'axios'

export default {
    //注册组件
    data(){
       return{
            disease_name: '',
            disease_icd: '',
            drug_type: '',
            drug_name: '',
            drug_atc: '',
            people: '',
            options:[{
                value: '1',
                label: '疾病'
            },{
                value: '2',
                label: '药品类型'
            },{
                value: '3',
                label: '药品'
            },{
                value: '4',
                label: '人群'
            }],
            value:'',         
       }      
    },

    methods:{
        AddInfo(){
            var type = ''
            var name = ''
            var attr = {}
            if(this.value === '1'){
                type = '疾病'
                name = this.disease_name
                attr = {
                    'icd11': this.disease_icd
                }
            }
            else if(this.value === '2'){
                type = '药品类型'
                name = this.drug_type
            }
            else if(this.value === '3'){
                type = '药品'
                name = this.drug_name
                attr = {
                    'atc': this.drug_atc
                }
            }
            else if(this.value === '4'){
                type = '人群'
                name = this.people
            }
            else{
                alert("ERROR")
            }

            const path = `http://localhost:5000/graph/create/node`

            axios
            .get(path,{
                params:{
                    'type': type,
                    'name': name,
                    'attr': attr
                }
            })
            .then(response => {
                var is_success = response.data.code
                if(is_success == 200){
                    alert("插入节点成功")
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

.add_msg{
    
    width:100%;
    
}


.add_label{
    float: center;
    margin-top:5%;
}

.add_input{
    width:100%;
    margin-top:2%;
    float:center;
    
}

.add_input input{
    width:250px;
    height:30px;
    padding-left:10px;
    margin-left:20px;
    margin-top:40px;
    font-size:16px;
}

.inform_btn{
    margin-top:50px;
}

</style>

