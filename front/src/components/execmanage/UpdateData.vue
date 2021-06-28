<template>
  <div>
    <!-- 面包屑导航区域 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>管理</el-breadcrumb-item>
      <el-breadcrumb-item>列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图区域 -->
    <el-card class="box-card">
      <el-button type="primary"
                 :loading="execinfoForm.isloading"
                 @click="updateDataMethod">
        点击更新
      </el-button>
      <el-divider>执行结果</el-divider>
      <!-- <el-input
        type="textarea"
        :rows="15"
        v-model="execinfoForm.execResult"></el-input> -->
      <span v-html="execinfoForm.execResult"></span>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      execinfoForm: {
        isloading: false,
        execResult: ''
      }
    }
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    async updateDataMethod () {
      this.execinfoForm.isloading = true
      this.execinfoForm.execResult = ''
      try {
        const { data: res } = await this.$http.get('exec_api/update_data')
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        this.execinfoForm.execResult = res.data.replace(/\n/g, '<br>')
        console.log(res.data)
      } catch (e) {
        const erroInfo = e.toString()
        if (erroInfo.indexOf('status code 401') !== -1) {
          this.logout()
          return this.$message.error('认证已过期,请重新登录')
        }
        return this.$message.error(erroInfo)
      }
      this.execinfoForm.isloading = false
      return this.$message.info('执行结束!')
    }
  }
}
</script>
<style>
</style>
