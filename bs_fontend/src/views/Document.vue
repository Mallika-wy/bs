<template>
    <v-md-preview :text="docText"></v-md-preview>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'

import { getDoc } from '@/api/api'


const docText = ref('')

onMounted(() => {
    getDoc().then(res => {
        docText.value = res.data
    })
})

</script>