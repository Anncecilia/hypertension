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
            <canvas v-for="page in pages" :id="'the-canvas'+page" :key="page"></canvas>
        </div>
    </div>
  </template>

<script>
 
    import PDFJS from 'pdfjs-dist'
    export default {
    
    data () {
      return {
        src: '../static/test.pdf', // pdf文件地址
        currentPage: 1, // pdf文件页码
        pageCount: 1, // pdf文件总页数
        fileType: 'pdf', // 文件类型
        pdfData:'../static/test.pdf',
        loadFinished:false,
        pages:"",
        pdfDoc:"",
      }
    },
    methods: {
        _renderPage (num) {
            this.pdfDoc.getPage(num).then((page) => {
            let canvas = document.getElementById('the-canvas' + num)
            let ctx = canvas.getContext('2d')
            let dpr = window.devicePixelRatio || 1
            let bsr = ctx.webkitBackingStorePixelRatio ||
                ctx.mozBackingStorePixelRatio ||
                ctx.msBackingStorePixelRatio ||
                ctx.oBackingStorePixelRatio ||
                ctx.backingStorePixelRatio || 1
            let ratio = dpr / bsr
            let viewport = page.getViewport(screen.availWidth / page.getViewport(1).width)
            canvas.width = viewport.width * ratio
            canvas.height = viewport.height * ratio
            canvas.style.width = viewport.width + 'px'
            canvas.style.height = viewport.height + 'px'
            ctx.setTransform(ratio, 0, 0, ratio, 0, 0)
            let renderContext = {
                canvasContext: ctx,
                viewport: viewport
            }
            page.render(renderContext)
            if (this.pages > num) {
                this._renderPage(num + 1)
            }
            })
        },
        _loadFile (url) {
            
            PDFJS.cMapUrl= 'https://unpkg.com/pdfjs-dist@2.0.943/cmaps/' // include "/"
            PDFJS.cMapPacked= true // set cMapPacked = true to ignore Warning: Ignoring invalid character "121" in hex string

            PDFJS.getDocument(url).promise.then((pdf) => {
                this.pdfDoc = pdf
                console.log(pdf)
                this.pages = this.pdfDoc.numPages
                this.$nextTick(() => {
                    this._renderPage(1)
                })
            })
        },
        /* previewPDF() {
            // 引入pdf.js的字体
            let CMAP_URL = 'https://unpkg.com/pdfjs-dist@2.0.943/cmaps/'
            //读取base64的pdf流文件
            let loadingTask = PDFJS.getDocument({
                data: this.pdfData, // PDF base64编码
                cMapUrl: CMAP_URL,
                cMapPacked: true
            })
            loadingTask.promise.then((pdf) => {
                this.loadFinished = true
                let numPages = pdf.numPages
                let pageNumber = 1
                this.getPage(pdf, pageNumber, numPages)
            })
        },
        getPage(pdf, pageNumber, numPages) {
            let _this = this
            pdf.getPage(pageNumber)
            .then((page) => {
                // 获取DOM中为预览PDF准备好的canvasDOM对象
                let canvas = this.$refs.myCanvas
                let viewport = page.getViewport(_this.scale)
                canvas.height = viewport.height
                canvas.width = viewport.width

                let ctx = canvas.getContext('2d')
                let renderContext = {
                    canvasContext: ctx,
                    viewport: viewport
                }
                page.render(renderContext).then(() => {
                    pageNumber += 1
                    if (pageNumber <= numPages) {
                    _this.getPage(pdf, pageNumber, numPages)
                    }
                })
            })
        } */
    },
    created:function () {
        // let src = require('../static/test.pdf') 
        let src = '../static/test.pdf'
        this._loadFile(src)
        //this.previewPDF()
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
</style>