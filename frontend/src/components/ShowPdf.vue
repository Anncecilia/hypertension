<template>
    <div>
        <div class='breadcrumb'>
            <el-breadcrumb separator="/" class="bc">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>查看所有文献</el-breadcrumb-item>
                <el-breadcrumb-item>完整文献预览及上传</el-breadcrumb-item>
                <el-breadcrumb-item>文献预览</el-breadcrumb-item>
                <router-link :to="{name: 'PdfList'}">
                    <div class="back-btn">
                        <el-button round size="mini">返回</el-button>
                    </div>
                </router-link> 
            </el-breadcrumb>
        </div>
        <div id="bar"></div>
        <div class="pdf" v-show="fileType === 'pdf'">
            <div class="page-top">
                <button @click="change1">上一页</button>
                {{currentPage}} / {{pageCount}}
                <button @click="change2">下一页</button>
                <br>
            </div>
            <pdf
                :src="src"
                :page="currentPage"
                @num-pages="pageCount = $event"
                @page-loaded="currentPage = $event"
                class="pdf-set"
            ></pdf>
            <div class="page-bottom">
                <button @click="change1">上一页</button>
                {{currentPage}} / {{pageCount}}
                <button @click="change2">下一页</button>
                <br>
            </div>
        </div>
    </div>
  </template>

  <script>
  import pdf from 'vue-pdf'
  
  export default {
    components: {pdf},
    data () {
      return {
        src: '../static/test.pdf', // pdf文件地址
        currentPage: 1, // pdf文件页码
        pageCount: 1, // pdf文件总页数
        fileType: 'pdf', // 文件类型
        btnFlag:false
      }
    },
    mounted () {
        window.addEventListener('scroll', this.scrollToTop)
    },
    destroyed () {
        window.removeEventListener('scroll', this.scrollToTop)
    },

    methods: {
        backTop () {
            const that = this
            let timer = setInterval(() => {
            let ispeed = Math.floor(-that.scrollTop / 5)
            document.documentElement.scrollTop = document.body.scrollTop = that.scrollTop + ispeed
            if (that.scrollTop === 0) {
                clearInterval(timer)
            }
            }, 16)
        },
        // 为了计算距离顶部的高度，当高度大于60显示回顶部图标，小于60则隐藏
    scrollToTop () {
        const that = this
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        that.scrollTop = scrollTop
        if (that.scrollTop > 60) {
            that.btnFlag = true
        } else {
            that.btnFlag = false
        }
    },
        change1(){
            if(this.currentPage>1){
                this.currentPage--
            }
            this.backTop()
        },
        change2(){
            if(this.currentPage < this.pageCount){
                this.currentPage++
            }
            this.backTop()
        }

    },
    created:function () {
        // 有时PDF文件地址会出现跨域的情况,这里最好处理一下
        this.src = pdf.createLoadingTask(this.src)
　　},
  }

</script>

<style scoped>
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
    .page-top{
        margin-top: 2%;
    }
    .page-bottom{
        margin-bottom: 2%;
    }
    body{
        background-color: #e5e5e5;
    }
</style>