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
        <el-table-column label="选项名" prop="label"></el-table-column>
        <!-- <el-table-column label="模板" prop="command"></el-table-column> -->
        <el-table-column label="操作" width="120px">
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
      <el-form :model="addform">
          <el-form-item label="选项名 : " :label-width="formLabelWidth">
            <el-input v-model="addform.label" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="脚本模板 : " :label-width="formLabelWidth">
            <el-input v-model="addform.command"  type="textarea" :rows="11" autocomplete="off"></el-input>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
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
      <el-form :model="modform">
          <el-form-item label="选项名 : " :label-width="formLabelWidth">
            <el-input v-model="modform.label" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="脚本模板 : " :label-width="formLabelWidth">
            <el-input v-model="modform.command"  type="textarea" :rows="11" autocomplete="off"></el-input>
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
      addform: {
        label: '',
        command: ''
      },
      modform: {
        id: '',
        label: '',
        command: ''
      },
      modDialogVisible: false,
      formLabelWidth: '120px'
    }
  },
  created () {
    this.getScriptList()
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    async getScriptList () {
      try {
        const { data: res } = await this.$http.get('query_script_temp', { params: this.queryInfo })
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        this.scriptlist = res.data.app_list
        this.total = res.data.total_rows
        // this.page_index = res.data.page_index
        this.queryInfo.page_index = res.data.page_index
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
      this.queryInfo.page_index = newPage
      this.getScriptList()
    },
    // 添加dialog关闭
    handleClose () {
      this.addform.label = ''
      this.addform.command = ''
      this.addDialogVisible = false
    },
    // 修改dialog关闭
    handleModClose () {
      this.modDialogVisible = false
      this.modform.id = -1
      this.modform.label = ''
      this.modform.command = ''
    },
    // 打开修改app的dialog
    handleModApp (scriptinfo) {
      this.modDialogVisible = true
      this.modform.id = scriptinfo.id
      this.modform.label = scriptinfo.label
      this.modform.command = scriptinfo.command
    },
    // 根据id删除数据
    handleDeleteApp (scriptinfo) {
      this.$confirm('确认删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async _ => {
        console.log(scriptinfo.id)
        this.DeleteId = scriptinfo.id
        const { data: res } = await this.$http.delete('delete_script_temp', { params: { id: this.DeleteId } })
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
      const { data: res } = await this.$http.post('add_script_temp', this.addform)
      if (res.meta.status !== 200) {
        return this.$message.error(res.meta.msg)
      } else {
        this.addform.label = ''
        this.addform.command = ''
        this.queryInfo.query_tag = 3
        this.getScriptList()
        this.queryInfo.query_tag = 0
        return this.$message.success('添加数据成功')
      }
    },
    async handleModSubmit () {
      const { data: res } = await this.$http.put('mod_script_temp', this.modform)
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
    }
  }
}
</script>

<style Lang="less" scoped>
  .card-input-select {
    width: 90px;
  }
</style>
