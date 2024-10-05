import { ElNotification } from 'element-plus'
import nprogress from 'nprogress'

export function notify(type, message) {
  ElNotification({
    message: message,
    type: type,
    duration: 5000
  })
}

// 显示全屏loading
export function showFullLoading(){
  nprogress.start()
}

// 隐藏全屏loading
export function hideFullLoading(){
  nprogress.done()
}
