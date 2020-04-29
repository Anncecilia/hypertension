<template>
    <div>
        <div class='disease_title'>
            <p>疾病</p>
        </div>
        <div class='disease_search'>
            <input v-model="searchVal" placeholder="请输入内容" class="disease_input">
            <el-button type="primary" icon="el-icon-search" @click="search_disease()" id="search_btn">搜索</el-button>
            
            <el-button type="primary" class="add_btn">添加数据</el-button>
            
        </div>
        
        <div class='disease_table'>
            <el-table 
            :data="tableData" heigt="500" border style="width:85%">
                <el-table-column prop="chapter_or_code" label="ICD-11编码" width="100"></el-table-column>
                <el-table-column prop="name" label="疾病名称" width="230"></el-table-column>
                <el-table-column prop="byname" label="别名" width="230"></el-table-column>
                <el-table-column prop="valid" label="是否为有效码（注意：标示为“否”者是章、节代码，或具有细分亚目的类目编码；在编码时应当采用有效码）" width="250"></el-table-column>
                <el-table-column prop="english" label="英文名" width="200"></el-table-column>
                <el-table-column fixed="right" label="操作" width="100">
                    
                    <template slot-scope="scope">
                        <el-button type="text" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <el-button type="text" size="small" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>
                    
                </el-table-column>
            </el-table>
        </div>
        
        
        
    </div>
    
</template>

<script type="text/javascript">

import axios from 'axios'

export default {
    //注册组件
    data(){
        return{
            
            searchVal:"",
            tableData: []
        }
    },
    

    methods:{
        handleEdit(index, row) {
            console.log(index, row);
        },
        handleDelete(index, row) {
            console.log(index, row);
        },
        getMongo(search) {
            const path = `http://localhost:5000/mongo/query`

            axios
            .get(path,{
                params:{
                    table: "disease",
                    msg: search
                }
            })
            .then(response => {
                var is_success = response.data.code
                if(is_success == 200){
                    this.tableData = response.data.data
                }
                else{
                    alert(response.data.msg)
                    this.tableData = []
                }
                
            })
            .catch(error => {
                console.log(error)
            })
        },
        search_disease(){
            var search = this.searchVal;
            this.getMongo(search);
            /* if (search){
                
            } */
        }
        
    }
    
}
</script>
<style type="text/css">
.disease_title{
    font-size: 32px;
    font-weight: bold;
    text-align: left;
    margin-left:13%;
    margin-top:100px;
}
.disease_search{
    width:74%;
    margin-left:13%;
    
}

.disease_input{
    float:left;
    height:25px;
    width:200px;
}

.disease_table{
    margin-left: 13%;
    margin-top:80px;
    
}

.add_btn{
    float: right;
    margin-left:100%;
}

#search_btn{
    float:left;
    margin-left:10px;
}


</style>

