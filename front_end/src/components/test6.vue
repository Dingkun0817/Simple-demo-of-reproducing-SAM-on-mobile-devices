<template>
  <div id="first-page">
    <div class="left">
      <div class="app">
        <h1>模型选择和图片上传</h1>
        <button @click="toggleModelSelection">模型选择</button>
    
        <!-- 显示模型选择按钮组 -->
        <div v-if="showModelSelection" class="model-buttons">
          <button v-on:click="runModel(1), upload()">运行SAM模型</button>
          <!-- <button @click="runModel(2)">运行模型2</button>
          <button @click="runModel(3)">运行模型3</button> -->
        </div>
    
        <!-- 文件上传输入框 -->
        <input type="file" ref="fileInput" style="display: none" @change="uploadImage" accept="image/*">
        <button v-on:click="openFileInput()">上传图片</button>
    
        <!-- 上传进度显示 -->
        <div v-if="uploading" class="upload-progress">
          <p>上传进度：</p>
          <progress :value="uploadProgress" max="100"></progress>
        </div>
    
        <!-- 上传完成后显示图片 -->
        <div v-if="uploadedImage" class="uploaded-image">
          <p>上传完成的图片：</p>
          <img :src="uploadedImage" alt="上传的图片">
        </div>
      </div>
    </div>
    <div class="right">
      <div v-if="imageUrl" class = "result-display">
        <!-- <img src="" alt="hhhhhhhhhhhhhhhhhh"> -->
        <!-- {{ imageUrl }} -->
        <!-- {{ res.data['message'] }} -->
        <img src="../assets/result/1.png" alt="hhhhhhhhhhhhhhhhhh">
      </div>
    </div>
  </div>

  </template>
  
  <script>
  import axios from 'axios'
  export default {
    data() {
      return {
        showModelSelection: false,   // 控制是否显示模型选择按钮组
        uploading: false,           // 控制是否显示上传进度
        uploadProgress: 0,          // 上传进度
        uploadedImage: null,        // 上传完成后显示的图片
        image_file: null,
        imageUrl: null,
      };
    },


    methods: {

      upload() {
        setTimeout( () => {
          const file = this.image_file
          // 创建FormData对象
          const formData = new FormData();
          formData.append('file', file);
          // 发送POST请求

          let requests = axios.create({
            //基础路径
            baseURL: 'http://127.0.0.1:8000',
            //请求不能超过5S
            timeout: 50000,
          });
          requests.post('/sam', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then((res) => {
            if (res.data) {
              try {
                const data = res.data['output']
                // Assuming that the image URL is stored in a property called 'image_url'
                if (data) {
                  let base = '../assets/result/'
                  this.imageUrl = data;
                  let name = '1.png'
                  this.imageUrl = base + name
                }
              } catch (error) {
                console.error('Error parsing ldk_data:', error);
              }
      }
          })
      }, 5000)
      console.log(1111);
      },
      // 切换模型选择按钮组的显示状态
      toggleModelSelection() {
        this.showModelSelection = !this.showModelSelection;
      },
      // 运行模型的方法，接受一个参数 modelNumber
      runModel(modelNumber) {
        // 在这里运行模型
        alert(`运行模型 ${modelNumber}`)  ;
      },
      // 打开文件上传输入框
      openFileInput() {
        this.$refs.fileInput.click();
        
      },
      // 处理文件上传事件
      uploadImage(event) {
        const file = event.target.files[0];
        console.log(file.name);
        if (file) {
          this.uploading = true;
          this.image_file = file
  
          // 模拟上传过程
          const uploadInterval = setInterval(() => {
            if (this.uploadProgress < 100) {
              this.uploadProgress += 10;
            } else {
              clearInterval(uploadInterval);
              this.uploading = false;
              this.uploadProgress = 0;
  
              // 上传完成后显示图片
              const reader = new FileReader();
              reader.onload = (e) => {
                this.uploadedImage = e.target.result;
                console.log(this.uploadedImage);
              };
              reader.readAsDataURL(file);
            }
          }, 500);
        }
      },
    },
  };
  </script>
  
  <style scoped>

#first-page{
    background-image: linear-gradient(
      90deg,
      cyan,
      purple
    );
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-size: 400%;
    animation: myanimation 10s infinite;
  }
@keyframes myanimation {
  0%{
    background-position: 0% 50%;
  }
  50%{
    background-position: 100% 50%;
  }
  100%{
    background-position: 0% 50%;
  }
}
  .app {
    text-align: center;
    margin: 200px;
    margin-top: 10px;
  }

  button {
    margin: 10px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .model-buttons {
    margin-top: 20px;
  }
  
  input[type="file"] {
    display: none;
  }
  
  .upload-progress {
    margin-top: 20px;
  }
  
  .uploaded-image {
    margin-top: 20px;
  }
  
  img {
    max-width: 100%;
  }

  .left {
  width: 60%;
  float: left;
}

.right {
  width: 40%;
  float: right;
  /* right: 50%;
  margin-left: 400px; */
}
  </style>
  
  
  
  
  
  <!-- <template>
      <div class="app">
        <h1>模型选择和图片上传</h1>
        <button @click="toggleModelSelection">模型选择</button>
  
        <div v-if="showModelSelection" class="model-buttons">
          <button @click="runModel(1)">运行模型1</button>
          <button @click="runModel(2)">运行模型2</button>
          <button @click="runModel(3)">运行模型3</button>
        </div>
  
        <input type="file" ref="fileInput" style="display: none" @change="uploadImage" accept="image/*">
        <button @click="openFileInput">上传图片</button>
  
        <div v-if="uploading" class="upload-progress">
          <p>上传进度：</p>
          <progress :value="uploadProgress" max="100"></progress>
        </div>
  
        <div v-if="uploadedImage" class="uploaded-image">
          <p>上传完成的图片：</p>
          <img :src="uploadedImage" alt="上传的图片">
        </div>
      </div>
    </template>
  
    <script>
    export default {
      data() {
        return {
          showModelSelection: false,
          uploading: false,
          uploadProgress: 0,
          uploadedImage: null,
        };
      },
      methods: {
        toggleModelSelection() {
          this.showModelSelection = !this.showModelSelection;
        },
        runModel(modelNumber) {
          // 在这里运行模型
          alert(`运行模型 ${modelNumber}`);
        },
        openFileInput() {
          this.$refs.fileInput.click();
        },
        uploadImage(event) {
          const file = event.target.files[0];
          if (file) {
            this.uploading = true;
  
            // 模拟上传过程
            const uploadInterval = setInterval(() => {
              if (this.uploadProgress < 100) {
                this.uploadProgress += 10;
              } else {
                clearInterval(uploadInterval);
                this.uploading = false;
                this.uploadProgress = 0;
  
                // 上传完成后显示图片
                const reader = new FileReader();
                reader.onload = (e) => {
                  this.uploadedImage = e.target.result;
                };
                reader.readAsDataURL(file);
              }
            }, 500);
          }
        },
      },
    };
    </script>
  
    <style scoped>
    .app {
      text-align: center;
      margin: 20px;
    }
  
    button {
      margin: 10px;
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #0056b3;
    }
  
    .model-buttons {
      margin-top: 20px;
    }
  
    input[type="file"] {
      display: none;
    }
  
    .upload-progress {
      margin-top: 20px;·
    }
  
    .uploaded-image {
      margin-top: 20px;
    }
  
    img {
      max-width: 100%;
    }
    </style>
     -->
  
