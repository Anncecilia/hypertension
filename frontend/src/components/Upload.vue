// Update.vue

<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>上传文献</el-breadcrumb-item>
                <div class="back-btn">
                    <el-button round size="mini" @click="TurnBack()">返回</el-button>
                </div>
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <div v-if="is_update" id="update_msg">
            <!-- <h2>
                目前没有已上传的文献信息!
            </h2> -->
            <el-upload
                class="upload-demo"
                drag
                ref="upload"
                action="http://localhost:5000/upload"
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :before-remove="beforeRemove"
                :on-success="handleSuccess"
                :file-list="fileList" 
                :headers="headers"
                :on-exceed="handleExceed"
                :before-upload="beforeUpload"
                accept="application/pdf"
                :on-change="handleChange"
                :http-request="submitUpload"
                multiple>
                <!-- :limit="3"
                    multiple
                :on-exceed="handleExceed"
                :auto-upload="false"
                action="https://jsonplaceholder.typicode.com/posts/"
                :before-upload="beforeUpload"
                :file-list="fileList"  -->
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <!-- <el-button size="small" type="primary">点击上传</el-button> -->
                <div slot="tip" class="el-upload__tip">只能上传pdf文件</div>
            </el-upload>
            <el-button style="margin-top: 5%;" size="medium" type="success" @click="submitUpload">上传到服务器</el-button>
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

            headers: {
                'Content-Type': 'multipart/form-data'
            },

            //所有文献是否都已提交更新
            is_update:true,
            /* fileList: [
                {name: 'food.jpeg', 
                url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
                }, 
                {name: 'food2.jpeg', 
                url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
                }
            ], */
            fileList:[],
            file : "",
            fileName: "",
        }
    },
    
    methods: {
        TurnBack(){
            this.$router.go(-1)
        },
        handleChange(file, fileList){
            console.log("on change")
            this.file = file;
            console.log(this.file)
            this.fileName = file.name;
            console.log(this.fileName)
        },
        beforeUpload(file){
            console.log("before upload")
            this.file = file;
            console.log(this.file)
            this.fileName = file.name;
            //return false // 返回false不会自动上传
        },
        handleRemove(file, fileList) {
            console.log(file);
        },
        //点击文件
        handlePreview(file) {
            console.log(file);
        },
        handleExceed(files, fileList) {
            this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
        },
        beforeRemove(file, fileList) {
            return this.$confirm(`确定移除 ${ file.name }？`);
        },
        handleSuccess(response, file, fileList){
            this.file = file
            alert("上传成功")
        },
        returnHome() {
            this.$router.push({
                path: '/home', 
                name:"Home",
            })
        },

    
        getPaperList() {
            const path = `http://localhost:5000/search/paper/update`
    
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
        submitUpload(){
            /* this.file = this.$refs.upload.uploadFiles
            console.log(this.file) */
            if(this.file == "" || this.fileName == ""){
                this.$message.warning('请选择要上传的文件！')
                return false
            }
            let fileFormData = new FormData();
            fileFormData.append('file', this.file, this.fileName);
            let requestConfig = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            }
            const path = `http://localhost:5000/upload`
            axios.post(path, fileFormData, requestConfig)
            .then(response => {
                this.result = response.data
                if(this.result.code == 200){
                    //alert(this.result.msg)
                    this.$message({
                        showClose: true,
                        message: this.result.msg,
                        type: 'success',
                        center: true
                    })
                    /* if(this.result.msg === '查询成功!'){
                        this.tableData = response.data.data
                        this.data_array = JSON.parse(JSON.stringify(this.result.data))
                        this.is_update = false
                    }
                    else{
                        this.is_update = true
                    }   */
                }
                else{
                    //alert("ERROR")
                    this.$message({
                        showClose: true,
                        message: this.result.msg,
                        center: true,
                        type: 'error'
                    })
                }    
            })
            .catch(error => {
                console.log(error)
            })
        }
    },

    created: function () {
        //this.getPaperList();
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
        margin-top: 5%;
    }
    </style>
    