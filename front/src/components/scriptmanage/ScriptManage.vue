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
      <!-- 数据列表区域 -->
      <el-table :data="scriptlist" :border="true" :stripe="true">
        <el-table-column label="#" type="index"></el-table-column>
        <el-table-column label="cluster_name" prop="cluster_name"></el-table-column>
        <el-table-column label="type_info" prop="type_info"></el-table-column>
        <el-table-column label="auto_key" prop="auto_key"></el-table-column>
        <!-- <el-table-column>
          <template v-slot="scope">
            <el-switch v-model="scope.row.mg_state" @change="userStateChange(scope.row)" activg_statee-color="#13ce66" inactive-color="#ff4949">
            </el-switch>
          </template>
        </el-table-column> -->
        <el-table-column label="操作" width="180px">
          <!-- <template v-slot="scope"> -->
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
            <!-- 查看按钮 -->
            <!-- <el-tooltip effect="dark" content="查看详情" placement="top"> -->
            <el-button
              type="warning"
              icon="el-icon-more-outline"
              v-model="scope.row.auto_key"
              @click="handleViewApp(scope.row)"
              size="mini">
            </el-button>
            <!-- </el-tooltip> -->
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
    <!-- 添加对话框 -->
    <el-dialog
      title="添加数据"
      v-model="addDialogVisible"
      width="50%"
      :show-close="false"
      :visible="addDialogVisible">
      <el-form :model="form">
          <el-form-item label="集群名 : " :label-width="formLabelWidth">
            <el-input v-model="form.cluster_name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="选择目录 : " :label-width="formLabelWidth">
            <el-select
              v-model="dirOptionValue"
              placeholder="请选择"
              @change='changeDirTag'>
              <el-option
                v-for="item in dirOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="目录名 : " :label-width="formLabelWidth">
            <el-input v-model="form.type_info" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="选择脚本模板 : " :label-width="formLabelWidth">
            <el-select
              v-model="scriptTempOptionValue"
              placeholder="请选择"
              @change='changeCommandTemp'>
              <el-option
                v-for="item in scriptTempOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="处理脚本 : " :label-width="formLabelWidth">
            <el-input v-model="form.command" type="textarea" :rows="11" autocomplete="off"></el-input>
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
          <el-form-item label="cluster_name : " :label-width="formLabelWidth">
            <el-input v-model="modform.cluster_name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="type_info : " :label-width="formLabelWidth">
            <el-input v-model="modform.type_info" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="command : " :label-width="formLabelWidth">
            <el-input v-model="modform.command" type="textarea" :rows="11" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleModClose">取 消</el-button>
          <el-button type="primary" @click="handleModSubmit">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 查看数据dialog -->
    <el-dialog
      title="查看数据"
      v-model="viewDialogVisible"
      width="50%"
      :show-close="false"
      :visible="viewDialogVisible">
      <el-form :model="viewform">
          <el-form-item label="cluster_name : " :label-width="formLabelWidth">
            <el-input :disabled="true" v-model="viewform.cluster_name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="type_info : " :label-width="formLabelWidth">
            <el-input :disabled="true" v-model="viewform.type_info" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="command : " :label-width="formLabelWidth">
            <el-input :disabled="true" type="textarea" :rows="11" v-model="viewform.command" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleViewClose">关 闭</el-button>
          <!-- <el-button type="primary" @click="handleModSubmit">确 定</el-button> -->
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
      // 目录选择
      dirOptions: [{
        value: '0',
        label: '无'
      }, {
        value: '5',
        label: '/'
      }, {
        value: '1',
        label: '/u01'
      }, {
        value: '2',
        label: '/u02'
      }, {
        value: '3',
        label: '/u03'
      }, {
        value: '4',
        label: '/var'
      }],
      dirOptionValue: '',
      searchOptionValue: '',
      // 脚本模板
      scriptTempOptions: [],
      scriptTempOptionValue: '',
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
      scriptlist: [],
      total: 0,
      // 添加dialog
      addDialogVisible: false,
      // 修改dialog
      modDialogVisible: false,
      // 查看
      viewDialogVisible: false,
      form: {
        auto_key: '',
        cluster_name: '',
        type_info: '',
        command: ''
      },
      modform: {
        auto_key: '',
        cluster_name: '',
        type_info: '',
        command: ''
      },
      viewform: {
        cluster_name: '',
        type_info: '',
        command: '',
        auto_key: ''
      },
      formLabelWidth: '120px'
    }
  },
  created () {
    this.getScriptList()
  },
  mounted () {
    this.getScriptTemp()
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    async getScriptList () {
      try {
        const { data: res } = await this.$http.get('query_script', { params: this.queryInfo })
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        this.scriptlist = res.data.app_list
        this.total = res.data.total_rows
        // this.page_index = res.data.page_index
        this.queryInfo.page_index = res.data.page_index
        console.log(res)
        console.log(this.scriptlist)
      } catch (e) {
        const erroInfo = e.toString()
        if (erroInfo.indexOf('status code 401') !== -1) {
          console.log('认证已过期,请重新登录')
          this.logout()
          return this.$message.error('认证已过期,请重新登录')
        }
        return this.$message.error(erroInfo)
      }
    },
    // 获取下拉框模板
    async getScriptTemp () {
      const { data: res } = await this.$http.get('get_all_script_temp')
      if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
      this.scriptTempOptions = res.data.option_list
    },
    // 搜索框清空时触发
    handleClear () {
      this.queryInfo.page_index = 1
      this.getScriptList()
    },
    // 点击搜索按钮时触发
    handleSearch () {
      if (this.queryInfo.query_tag !== 2) {
        this.queryInfo.query_tag = 1
      } else {
        this.changeQueryTag()
      }
      this.getScriptList()
    },
    // 监听pageszie 改变的事件
    handleSizeChange (newSize) {
      // console.log(newSize)
      this.queryInfo.page_size = newSize
      this.getScriptList()
    },
    // 监听页码值改变
    handleCurrentChange (newPage) {
      // console.log(newPage)
      this.queryInfo.page_index = newPage
      this.getScriptList()
    },
    // 添加dialog关闭
    handleClose () {
      this.form.auto_key = ''
      this.form.cluster_name = ''
      this.form.command = ''
      this.form.type_info = ''
      this.addDialogVisible = false
    },
    // 修改dialog关闭
    handleModClose () {
      this.modDialogVisible = false
      this.modform.auto_key = -1
      this.modform.cluster_name = ''
      this.modform.type_info = ''
      this.modform.command = ''
    },
    // 查看dialog关闭
    handleViewClose () {
      this.viewDialogVisible = false
      this.viewform.auto_key = -1
      this.viewform.cluster_name = ''
      this.viewform.type_info = ''
      this.viewform.command = ''
    },
    // 打开修改app的dialog
    handleModApp (scriptinfo) {
      console.log(scriptinfo)
      this.modDialogVisible = true
      this.modform.cluster_name = scriptinfo.cluster_name
      this.modform.type_info = scriptinfo.type_info
      this.modform.command = scriptinfo.command
      this.modform.auto_key = scriptinfo.auto_key
    },
    // 根据auto-key查看
    handleViewApp (scriptinfo) {
      console.log(scriptinfo)
      this.viewDialogVisible = true
      this.viewform.auto_key = scriptinfo.auto_key
      this.viewform.type_info = scriptinfo.type_info
      this.viewform.cluster_name = scriptinfo.cluster_name
      this.viewform.command = scriptinfo.command
    },
    // 根据appid删除数据
    handleDeleteApp (scriptinfo) {
      this.$confirm('确认删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async _ => {
        console.log(scriptinfo.auto_key)
        this.DeleteInfo = scriptinfo.auto_key
        const { data: res } = await this.$http.delete('delete_script', { params: { auto_key: this.DeleteInfo } })
        console.log(res)
        if (res.meta.status !== 200) {
          return this.$message.error(res.meta.msg)
        } else {
          this.getScriptList()
          return this.$message.success('删除数据成功')
        }
      }).catch(_ => {})
    },
    // 数据存入数据库
    async handleSubmit () {
      const { data: res } = await this.$http.post('add_script', this.form)
      if (res.meta.status !== 200) {
        return this.$message.error(res.meta.msg)
      } else {
        this.form.ip = ''
        this.form.cluster_info = ''
        this.queryInfo.query_tag = 3
        this.getScriptList()
        this.queryInfo.query_tag = 0
        return this.$message.success('添加数据成功')
      }
    },
    async handleModSubmit () {
      const { data: res } = await this.$http.put('mod_script', this.modform)
      if (res.meta.status !== 200) {
        return this.$message.error(res.meta.msg)
      } else {
        this.handleModClose()
        this.getScriptList()
        return this.$message.success('修改数据成功')
      }
    },
    changeQueryTag () {
      this.queryInfo.query_tag = this.searchOptionValue
      console.log(this.queryInfo.query_tag)
    },
    changeCommandTemp () {
      console.log(this.scriptTempOptionValue)
      const optionRow = this.scriptTempOptions.filter((row) => {
        return row.value === this.scriptTempOptionValue
      })
      this.form.command = optionRow[0].command
    },
    changeDirTag () {
      if (this.dirOptionValue === '0') {
        this.form.type_info = ''
      }
      if (this.dirOptionValue === '1') {
        this.form.type_info = '/u01'
      }
      if (this.dirOptionValue === '2') {
        this.form.type_info = '/u02'
      }
      if (this.dirOptionValue === '3') {
        this.form.type_info = '/u03'
      }
      if (this.dirOptionValue === '4') {
        this.form.type_info = '/var'
      }
      if (this.dirOptionValue === '5') {
        this.form.type_info = '/'
      }
    }
  }
}
</script>

<style Lang="less" scoped>
  .card-input-select {
    width: 90px;
  }
</style>
