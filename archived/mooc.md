# container for mooc

```
# 30890 is web vnc
docker run -d -p 30890:5800 --name cus0 --shm-size 2g recolic/firefox-vnc-wangke

# 30890 is bare vnc
docker run -tid -p 30894:5900 --name cus0 recolic/chrome-vnc-wangke
```
