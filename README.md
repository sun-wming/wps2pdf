# wps2pdf
1. 构建基础镜像
```
docker build --no-cache  -f  image_base/Dockerfile  -t  debian_wps:base  .
```

2.构建业务镜像
```
docker build --no-cache -t py_wps_2_pdf:latest .
```
