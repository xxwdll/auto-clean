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
      <!-- <el-form ref="loginFormRef" :model="resetPassForm" :rules="resetPassFormRules" label-width="0px" class='login_form'>
        <el-row :gutter="20">
          <el-col :span="7">
            <el-input placeholder="当前密码"
            :clearable="true"
            type='password'>
              <template #append>
              </template>
            </el-input>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="7">
            <el-input placeholder="新密码"
            :clearable="true"
            type='password'>
              <template #append>
              </template>
            </el-input>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="7">
            <el-input placeholder="再次输入新密码"
            :clearable="true"
            type='password'>
              <template #append>
              </template>
            </el-input>
          </el-col>
        </el-row>
        <el-form-item label="" class='btn-s'>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-button type='primary' @click='login'>登录</el-button>
              <el-button type='info' @click='resetloginForm'>重置</el-button>
            </el-col>
          </el-row>
        </el-form-item>
      </el-form> -->
      <!-- form表单区域 -->
      <el-form ref="resetPassFormRef" :model="resetPassForm" :rules="RestPassFormRules" label-width="0px" class='login_form'>
        <!-- 密码 -->
        <el-form-item prop="password">
          <!-- <el-input prefix-icon="el-icon-unlockss"></el-input> -->
          <el-input v-model="resetPassForm.password"
                    prefix-icon="el-icon-lock"
                    placeholder="当前密码"
                    type='password'>
          </el-input>
        </el-form-item>
        <!-- 确认密码 -->
        <el-form-item prop="newpassword">
          <el-input v-model="resetPassForm.newpassword"
                    prefix-icon="el-icon-lock"
                    placeholder="新密码"
                    type='password'>
          </el-input>
        </el-form-item>
        <!-- 确认新密码 -->
        <el-form-item prop="checknewpassword">
          <el-input v-model="resetPassForm.checknewpassword"
                    prefix-icon="el-icon-lock"
                    placeholder="请再次确认新密码"
                    type='password'>
          </el-input>
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item label="" class='btn-s'>
          <el-button type='primary' @click='passConfirm'>提交</el-button>
          <el-button type='info' @click='resetPassFormMethod'>重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <!-- 确认对话框 -->
    <el-dialog
      title="提示"
      v-model="addDialogVisible"
      width="30%"
      :visible="addDialogVisible">
      <span>这是一段信息</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="addDialogVisible = false">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.RestPassFormRules.newpassword) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      resetPassForm: {
        password: '',
        newpassword: '',
        checknewpassword: ''
      },
      // 表单的验证规则
      RestPassFormRules: {
        password: [
          { required: true, message: '请输入当前密码', trigger: 'blur' },
          { min: 4, max: 15, message: '长度在 4 到 15 个字符', trigger: 'blur' }
        ],
        newpassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 4, max: 15, message: '长度在 4 到 15 个字符', trigger: 'blur' }
        ],
        checknewpassword: [
          /* { required: true, message: '请输入新密码', trigger: 'blur' }, */
          { validator: validatePass2, trigger: 'blur' },
          { min: 4, max: 15, message: '长度在 4 到 15 个字符', trigger: 'blur' }
        ]
      },
      addDialogVisible: false
    }
  },
  /* created () {
    this.getUserList()
  }, */
  methods: {
    // 重置表单数据按钮
    resetPassFormMethod () {
      this.$refs.resetPassFormRef.resetFields()
    },
    passConfirm () {
      console.log('pass')
    }
  }
}
</script>
<style>
  /* .btn-s {
    display: flex;
    justify-content: flex-end;
  } */
  .login_form {
    /* position: absolute;
    bottom: 0; */
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }
</style>
