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


export function addTb(id, infoTBJD) {
    return axios.post("/addTb", {
        id,
        infoTBJD
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

export function addJd(id) {
    return axios.post("/addJd", {
        user_id: id
    })
}

export function getQrcode() {
    return axios.get("/getQrcode", {
        params: {
        }
    })
}