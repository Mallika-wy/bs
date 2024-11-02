import axios from "@/axios"


export function login(name, password) {
    return axios.post("/login", {
        name,
        password
    })
}


export function modifyUser(id, modifiedUser) {
    return axios.post("/modifyUser", {
        id,
        modifiedUser
    })
}


export function addTb(user_id, info_tb) {
    return axios.post("/addTb", {
        user_id,
        info_tb
    })
}

export function test() {
    return axios.post("/test", {
    })
}



export function searchItem(id, searchText) {
    return axios.get("/search", {
        params: {
            id: id, // 假设的 ID 值
            searchText: searchText // 假设的搜索文本
        }
    })
}

export function addJd(user_id) {
    return axios.post("/addJd", {
        user_id
    })
}

export function getQrcode() {
    return axios.get("/getQrcode", {
        params: {
        }
    })
}

export function getDoc() {
    return axios.get("/getDoc", {
        params: {
        }
    })
}

export function register(user_info_dict) {
    return axios.post("/register", {
        user_info_dict
    })
}