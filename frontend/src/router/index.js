import Vue from 'vue'

import Router from 'vue-router'

const routerOptions = [

{ path: '/', component: 'HomePage' , name:"HomePage", meta: { navShow: true}},
{ path: '/home', component: 'Home' , name:"Home", meta: { navShow: true}},
{ path: "/login",component: 'Login', name:"Login", meta: { navShow: false}},
{ path: "/register",component: 'Register', name:"Register", meta: { navShow: false}},
{ path: "/disease",component: 'Disease', name:"Disease", meta: { navShow: true}},
{ path: "/addnode",component: 'AddNode', name:"AddNode", meta: { navShow: true}},
{ path: "/addrelation",component: 'AddRelation', name:"AddRelation", meta: { navShow: true}},
{ path: "/spider",component: 'Spider', name:"Spider", meta: { navShow: true}},
{ path: "/paper/all",component: 'AllPaper', name:"AllPaper", meta: { navShow: true}},
{ path: "/paper/unmark/list",component: 'UnmarkPaperList', name:"UnmarkPaperList", meta: { navShow: true}},
{ path: "/paper/unmark/detail",component: 'PaperDetail', name:"PaperDetail", meta: { navShow: true}},
{ path: "/update",component: 'Update', name:"Update", meta: { navShow: true}},
{ path: "/paper/mark/list",component: 'MarkPaperList', name:"MarkPaperList", meta: { navShow: true}},
{ path: "/paper/mark/detail",component: 'MarkPaperDetail', name:"MarkPaperDetail", meta: { navShow: true}},
{ path: "/paper/upload",component: 'Upload', name:"Upload", meta: { navShow: true}},
{ path: "/paper/pdf/detail",component: 'pdf', name:"pdf", meta: { navShow: true}},
{ path: "/paper/pdf/list",component: 'PdfList', name:"PdfList", meta: { navShow: true}},
{ path: "/show/pdf",component: 'ShowPdf', name:"ShowPdf", meta: { navShow: true}},

]

const routes = routerOptions.map(route => {

return {

...route,

component: () => import(`@/components/${route.component}.vue`)

}

})

Vue.use(Router)

export default new Router({

routes,

mode: 'history'

})