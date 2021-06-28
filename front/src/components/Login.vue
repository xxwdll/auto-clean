<template>
  <div class="login_container">
    <div class="login_box">
      <!-- 头像区域 -->
      <div class="avatar_box">
        <img src="../assets/logo.png" />
      </div>
      <!-- form表单区域 -->
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="0px" class='login_form'>
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" prefix-icon="el-icon-user-solid"></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="password">
          <!-- <el-input prefix-icon="el-icon-unlockss"></el-input> -->
          <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" type='password'></el-input>
        </el-form-item>
        <!-- 按钮区域 -->
        <el-form-item label="" class='btn-s'>
          <el-button type='primary' @click='login'>登录</el-button>
          <el-button type='info' @click='resetloginForm'>重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 登录表单数据绑定对象
      loginForm: {
        username: '',
        password: ''
      },
      // 表单的验证规则
      loginFormRules: {
        username: [
          { required: true, message: '请输入登录名称', trigger: 'blur' },
          { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入登录密码', trigger: 'blur' },
          { min: 4, max: 15, message: '长度在 4 到 15 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    const tokenStr = sessionStorage.getItem('token')
    if (tokenStr) return this.$router.push('/home')
  },
  methods: {
    // 重置表单数据按钮
    resetloginForm () {
      this.$refs.loginFormRef.resetFields()
    },
    login () {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (valid) {
          const { data: res } = await this.$http.post('login', this.loginForm)
          // console.log(res)
          if (res.meta.status !== 200) {
            return this.$message.error('登录失败')
          } else {
            this.$message.success('登陆成功')
            console.log(res.data)
            window.sessionStorage.setItem('token', res.data.token)
            this.$router.push('/home')
          }
          // console.log(res)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style Lang="less" scoped>
  .login_container{
    background-color: #2b4b6b;
    height: 100%;
  }
  .login_box {
    width: 450px;
    height: 300px;
    background-color: #FFFFFF;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  .avatar_box {
    height: 130px;
    width: 130px;
    border: 1px solid #eee;
    border-radius: 50%;
    padding: 10px;
    box-shadow: 0 0 10px #ddd;
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #FFFFFF;
  }
  .avatar_box img {
    height: 100%;
    width: 100%;
    border-radius: 50%;
    background-color: #EEEEEE;
  }
  .btn-s {
    display: flex;
    justify-content: flex-end;
  }
  .login_form {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }
</style>
