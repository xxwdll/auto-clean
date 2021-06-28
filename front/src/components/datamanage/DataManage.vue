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
      <!-- 输入框 -->
      <el-row :gutter="20">
        <el-col :span="10">
          <el-input placeholder="请输入内容"
          v-model="queryInfo.query"
          :clearable="true"
          @clear="handleClear">
            <el-select v-model="searchOptionValue"
              slot="prepend"
              placeholder="请选择"
              class="card-input-select"
              @change='changeQueryTag'>
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <template #append>
              <el-button icon="el-icon-search"
              @click="handleSearch">
              </el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary"
          @click="addDialogVisible = true">
          添加数据
          </el-button>
        </el-col>
      </el-row>
      <!-- 用户列表区域 -->
      <el-table :data="applist" :border="true" :stripe="true">
        <el-table-column label="#" type="index"></el-table-column>
        <el-table-column label="ip" prop="ip"></el-table-column>
        <el-table-column label="cluster_info" prop="cluster_info"></el-table-column>
        <el-table-column label="操作" width="120px">
          <template v-slot="scope">
            <!-- 編輯按鈕 -->
            <el-button
              type="primary"
              icon="el-icon-edit"
              @click="handleModApp(scope.row)"
              size="mini">
            </el-button>
            <!-- 删除按钮 -->
            <el-button
              v-model="scope.row.app_id"
              @click="handleDeleteApp(scope.row)"
              type="danger"
              icon="el-icon-delete"
              size="mini">
            </el-button>
            <!-- 分配按钮 -->
            <!-- <el-tooltip effect="dark" content="分配权限" placement="top">
              <el-button type="warning" icon="el-icon-setting" size="mini"></el-button>
            </el-tooltip> -->
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryInfo.page_index"
            :page-sizes="[5, 10, 20, 50]"
            :page-size="queryInfo.page_size"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
          </el-pagination>
    </el-card>
    <!-- 用户对话框 -->
    <el-dialog
      title="添加数据"
      v-model="addDialogVisible"
      width="50%"
      :show-close="false"
      :visible="addDialogVisible">
      <el-form :model="form">
          <el-form-item label="ip : " :label-width="formLabelWidth">
            <el-input v-model="form.ip" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="集群名 : " :label-width="formLabelWidth">
            <el-input v-model="form.cluster_info" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <!-- <el-button @click="addDialogVisible = false">取 消</el-button> -->
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="handleSubmit">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 修改数据dialog -->
    <el-dialog
      title="修改数据"
      v-model="modDialogVisible"
      width="50%"
      :show-close="false"
      :visible="modDialogVisible">
      <el-form :model="form">
          <el-form-item label="ip : " :label-width="formLabelWidth">
            <el-input v-model="modform.ip" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="集群名 : " :label-width="formLabelWidth">
            <el-input v-model="modform.cluster_info" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleModClose">取 消</el-button>
          <el-button type="primary" @click="handleModSubmit">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 下拉选项
      options: [{
        value: '1',
        label: '模糊'
      }, {
        value: '2',
        label: '全量'
      }],
      searchOptionValue: '',
      // 获取列表的参数对象
      queryInfo: {
        query: '',
        // tag 0 无含义, 1 模糊, 2 全量, 3 查询数据的当前页数据
        query_tag: 0,
        // 当前页数
        page_index: 1,
        // 当前每页显示多少条
        page_size: 10
      },
      applist: [],
      total: 0,
      // 添加dialog
      addDialogVisible: false,
      // 修改dialog
      modDialogVisible: false,
      form: {
        ip: '',
        cluster_info: '',
        app_id: ''
      },
      modform: {
        ip: '',
        cluster_info: ''
      },
      formLabelWidth: '120px'
    }
  },
  created () {
    this.getAppList()
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    async getAppList () {
      try {
        const { data: res } = await this.$http.get('query_app', { params: this.queryInfo })
        // const { data: res } = await this.$http.post('query_app', this.queryInfo)
        // console.log(res)
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        this.applist = res.data.app_list
        this.total = res.data.total_rows
        // this.page_index = res.data.page_index
        this.queryInfo.page_index = res.data.page_index
        console.log(res)
        console.log(this.applist)
      } catch (e) {
        this.$message.error(e.toString())
        console.log(e)
        const erroInfo = e.toString()
        if (erroInfo.indexOf('status code 401') !== -1) {
          console.log('认证已过期,请重新登录')
          this.logout()
          return this.$message.error('认证已过期,请重新登录')
        }
        return this.$message.error(erroInfo)
      }
    },
    // 搜索框清空时触发
    handleClear () {
      this.queryInfo.page_index = 1
      this.getAppList()
    },
    // 点击搜索按钮时触发
    handleSearch () {
      if (this.queryInfo.query_tag !== 2) {
        this.queryInfo.query_tag = 1
      } else {
        this.changeQueryTag()
      }
      this.getAppList()
    },
    // 监听pageszie 改变的事件
    handleSizeChange (newSize) {
      // console.log(newSize)
      this.queryInfo.page_size = newSize
      this.getAppList()
    },
    // 监听页码值改变
    handleCurrentChange (newPage) {
      // console.log(newPage)
      this.queryInfo.page_index = newPage
      this.getAppList()
    },
    // 添加dialog关闭
    handleClose () {
      this.addDialogVisible = false
      this.modform.ip = ''
      this.modform.cluster_info = ''
    },
    // 修改dialog关闭
    handleModClose () {
      this.modDialogVisible = false
      this.modform.ip = ''
      this.modform.cluster_info = ''
      this.modform.app_id = -1
    },
    // 打开修改app的dialog
    handleModApp (appinfo) {
      console.log(appinfo)
      this.modDialogVisible = true
      this.modform.ip = appinfo.ip
      this.modform.cluster_info = appinfo.cluster_info
      this.modform.app_id = appinfo.app_id
    },
    // 根据appid删除数据
    handleDeleteApp (appinfo) {
      this.$confirm('确认删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async _ => {
        console.log(appinfo.app_id)
        this.DeleteInfo = appinfo.app_id
        const { data: res } = await this.$http.delete('delete_app', { params: { app_id: this.DeleteInfo } })
        console.log(res)
        if (res.meta.status !== 200) {
          return this.$message.error(res.meta.msg)
        } else {
          this.getAppList()
          return this.$message.success('删除数据成功')
        }
      }).catch(_ => {})
    },
    // 数据存入数据库
    async handleSubmit () {
      const { data: res } = await this.$http.post('add_app', this.form)
      if (res.meta.status !== 200) {
        return this.$message.error(res.meta.msg)
      } else {
        this.form.ip = ''
        this.form.cluster_info = ''
        this.queryInfo.query_tag = 3
        this.getAppList()
        this.queryInfo.query_tag = 0
        return this.$message.success('添加数据成功')
      }
    },
    async handleModSubmit () {
      const { data: res } = await this.$http.put('mod_app', this.modform)
      if (res.meta.status !== 200) {
        return this.$message.error(res.meta.msg)
      } else {
        this.handleModClose()
        this.getAppList()
        return this.$message.success('修改数据成功')
      }
    },
    changeQueryTag () {
      this.queryInfo.query_tag = this.searchOptionValue
      console.log(this.queryInfo.query_tag)
    }
  }
}
</script>

<style Lang="less" scoped>
  .card-input-select {
    width: 90px;
  }
</style>
