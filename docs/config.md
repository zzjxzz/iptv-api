| 配置项                    | 描述                                                                                        | 默认值                                     |
|:-----------------------|:------------------------------------------------------------------------------------------|:----------------------------------------|
| open_driver            | 开启浏览器运行，若更新无数据可开启此模式，较消耗性能                                                                | False                                   |
| open_empty_category    | 开启无结果频道分类，自动归类至底部                                                                         | False                                   |
| open_filter_resolution | 开启分辨率过滤，低于最小分辨率（min_resolution）的接口将会被过滤                                                   | True                                    |
| open_filter_speed      | 开启速率过滤，低于最小速率（min_speed）的接口将会被过滤                                                          | True                                    |
| open_hotel             | 开启酒店源功能，关闭后所有酒店源工作模式都将关闭                                                                  | True                                    |
| open_hotel_foodie      | 开启 Foodie 酒店源工作模式                                                                         | True                                    |
| open_hotel_fofa        | 开启 FOFA、ZoomEye 酒店源工作模式                                                                   | True                                    |
| open_keep_all          | 开启保留所有检索结果，会保留非模板频道名称的结果，推荐手动维护时开启                                                        | False                                   |
| open_m3u_result        | 开启转换生成 m3u 文件类型结果链接，支持显示频道图标                                                              | True                                    |
| open_multicast         | 开启组播源功能，关闭后所有组播源工作模式都将关闭                                                                  | True                                    |
| open_multicast_foodie  | 开启 Foodie 组播源工作模式                                                                         | True                                    |
| open_multicast_fofa    | 开启 FOFA 组播源工作模式                                                                           | True                                    |
| open_online_search     | 开启关键字搜索源功能                                                                                | False                                   |
| open_proxy             | 开启代理，自动获取免费可用代理，若更新无数据可开启此模式                                                              | False                                   |
| open_request           | 开启查询请求，数据来源于网络（仅针对酒店源与组播源）                                                                | False                                   |
| open_service           | 开启页面服务，用于控制是否启动结果页面服务；如果使用青龙等平台部署，有专门设定的定时任务，需要更新完成后停止运行，可以关闭该功能                          | True                                    |
| open_sort              | 开启排序功能（响应速度、日期、分辨率）                                                                       | True                                    |
| open_subscribe         | 开启订阅源功能                                                                                   | False                                   |
| open_update            | 开启更新，用于控制是否更新接口，若关闭则所有工作模式（获取接口和测速）均停止                                                    | True                                    |
| open_update_time       | 开启显示更新时间                                                                                  | True                                    |
| open_url_info          | 开启显示接口说明信息，用于控制是否显示分辨率、接口协议类型等信息，为$符号后的内容，播放软件使用该信息对接口进行描述                                | True                                    |
| open_use_cache         | 开启使用本地缓存数据，适用于查询请求失败场景（仅针对酒店源与组播源）                                                        | True                                    |
| open_use_old_result    | 开启使用历史更新结果（包含模板与结果文件的接口），合并至本次更新中                                                         | True                                    |
| final_file             | 生成结果文件路径                                                                                  | output/result.txt                       |
| hotel_num              | 结果中偏好的酒店源接口数量                                                                             | 4                                       |
| hotel_page_num         | 酒店地区获取分页数量                                                                                | 1                                       |
| hotel_region_list      | 酒店源地区列表，"全部"表示所有地区                                                                        | 全部                                      |
| ipv4_num               | 结果中偏好的 IPv4 接口数量                                                                          | 5                                       |
| ipv6_num               | 结果中偏好的 IPv6 接口数量                                                                          | 5                                       |
| ipv6_support           | 强制认为当前网络支持IPv6，跳过检测                                                                       | False                                   |
| ipv_type               | 生成结果中接口的协议类型，可选值：ipv4、ipv6、全部、all                                                         | 全部                                      |
| ipv_type_prefer        | 接口协议类型偏好，优先将该类型的接口排在结果前面，可选值：IPv4、IPv6、自动、auto                                            | 自动                                      |
| min_resolution         | 接口最小分辨率，需要开启 open_filter_resolution 才能生效                                                  | 1920x1080                               |
| min_speed              | 接口最小速率（单位M/s），需要开启 open_filter_speed 才能生效                                                 | 0.2                                     |
| multicast_num          | 结果中偏好的组播源接口数量                                                                             | 3                                       |
| multicast_page_num     | 组播地区获取分页数量                                                                                | 1                                       |
| multicast_region_list  | 组播源地区列表，"全部"表示所有地区                                                                        | 全部                                      |
| online_search_num      | 结果中偏好的关键字搜索接口数量                                                                           | 0                                       |
| online_search_page_num | 关键字搜索频道获取分页数量                                                                             | 1                                       |
| origin_type_prefer     | 结果偏好的接口来源，结果优先按该顺序进行排序，hotel：酒店源，multicast：组播源，subscribe：订阅源，online_search：关键字搜索          | hotel,multicast,subscribe,online_search |
| recent_days            | 获取最近时间范围内更新的接口（单位天），适当减小可避免出现匹配问题                                                         | 30                                      |
| request_timeout        | 查询请求超时时长，单位秒(s)，用于控制查询接口文本链接的超时时长以及重试时长，调整此值能优化更新时间                                       | 10                                      |
| sort_timeout           | 单个接口测速超时时长，单位秒(s)；数值越大测速所属时间越长，能提高获取接口数量，但质量会有所下降；数值越小测速所需时间越短，能获取低延时的接口，质量较好；调整此值能优化更新时间 | 10                                      |
| source_file            | 模板文件路径                                                                                    | config/demo.txt                         |
| subscribe_num          | 结果中偏好的订阅源接口数量                                                                             | 3                                       |
| urls_limit             | 单个频道接口数量                                                                                  | 10                                      |