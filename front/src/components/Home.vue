<template>
   <el-container class='home-container'>
     <!-- 头部区域 -->
     <el-header>
       <div>
         <img id="home_log_png" src="../assets/logo.png" alt=""/>
         <span>AAA</span>
       </div>
       <el-button type="info" @click='logout'>退出</el-button>
     </el-header>
     <!-- 页面主体区域 -->
     <el-container>
       <!-- 侧边栏 -->
       <el-aside :width="isCollapse ? '64px' : '200px'">
         <div class="toggle" @click="toggleCollapse">|||</div>
         <!-- 侧边栏菜单区域 -->
         <el-menu background-color="#333744"
               text-color="#fff"
               active-text-color="#409BFF"
               :unique-opened="true"
               :collapse="isCollapse"
               :collapse-transition="false"
               :router="true"
               :default-active="activePath">
               <!-- 一级菜单 -->
               <el-submenu :index="item.id + ''" v-for="item in menulist" :key="item.id">
                 <!-- 一级菜单模板区域 -->
                 <template slot="title">
                   <!-- 图标 -->
                   <i :class="iconsObj[item.id]"></i>
                   <!-- 文本 -->
                   <span>{{ item.authName }}</span>
                 </template>
                 <!-- 二级菜单 -->
                 <el-menu-item :index="'/' +subItem.path" v-for="subItem in item.children"
                               :key="subItem.id" @click="saveNavState('/' +subItem.path)">
                   <template slot="title">
                     <!-- 图标 -->
                     <i class="el-icon-menu"></i>
                     <!-- 文本 -->
                     <span>{{ subItem.authName }}</span>
                   </template>
                 </el-menu-item>
               </el-submenu>
             </el-menu>
       </el-aside>
       <!-- 右侧主体 -->
       <el-main>
         <!-- 路由占位符 -->
         <router-view></router-view>
       </el-main>
     </el-container>
   </el-container>
</template>

<script>
export default {
  data () {
    return {
      // 左菜单栏
      menulist: [],
      iconsObj: {
        // user
        125: 'el-icon-user-solid',
        // box
        103: 'el-icon-box',
        // shop
        101: 'el-icon-shopping-bag-1',
        // order
        102: 'el-icon-document',
        // data line
        145: 'el-icon-data-line'
      },
      isCollapse: false,
      // 激活的地址
      activePath: ''
    }
  },
  created () {
    this.getMenuList()
    this.activePath = sessionStorage.getItem('activePath')
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    /* 获取所有的菜单 */
    async getMenuList () {
      try {
        const { data: res } = await this.$http.get('menus')
        if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
        this.menulist = res.data
      } catch (e) {
        console.log(e)
        this.$message.error('token过期,请重新登录')
        this.logout()
      }
      /* const { data: res } = await this.$http.get('menus')
      if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
      this.menulist = res.data
      console.log(res.data) */
    },
    // 切换菜单的折叠与展开
    toggleCollapse () {
      this.isCollapse = !this.isCollapse
    },
    // 保存链接的激活状态
    saveNavState (activePath) {
      window.sessionStorage.setItem('activePath', activePath)
      this.activePath = activePath
    }
  }
}
</script>

<style Lang="less" scoped>
  .el-header {
    background-color: #373D41;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #FFFFFF;
    font-size: 20px;
  }
  .el-header div {
    display: flex;
    align-items: center;
  }
  .el-header div span {
     margin-left: 15px;
  }
  .el-aside {
    background-color: #333744;
  }
  .toggle {
    background-color: #4A5064;
    font-size: 0.625rem;
    line-height: 1.5rem;
    color: #FFFFFF;
    text-align: center;
    letter-spacing: 0.2em;
    cursor: pointer;
  }
  .el-aside .el-menu {
    border-right: 0px;
  }
  .el-main {
    background-color: #EAEDF1;
  }
  .home-container {
    height: 100%;
  }
  #home_log_png {
    height: 60px;
    width: 60px;
  }
</style>
