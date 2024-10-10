import router from './router'
import { getToken } from "@/composables/cookie"
import { useStore } from 'vuex'
import { notify, showFullLoading, hideFullLoading } from "@/composables/utils"

// 全局前置守卫
router.beforeEach(async (to,from,next)=>{
    showFullLoading()

    const store = useStore()
    const token = getToken()
    const user = store.state.user
    console.log(token)
    console.log(user)
    // 没有登录，强制跳转回登录页
    if((!token || !user.id) && to.path != "/login"){
        notify("error","请先登录")
        return next({ path:"/login" })
    }

    
    // 设置标题
    let title = (to.meta.title ? to.meta.title : "")
    document.title = title
    
    next()
})


// 全局后置守卫
router.afterEach((to, from) => hideFullLoading())