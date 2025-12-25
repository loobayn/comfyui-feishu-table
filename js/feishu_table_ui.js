/**
 * ComfyUI 飞书多维表格插件前端扩展
 * 提供更好的用户界面和交互体验
 */

import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// 扩展飞书表格节点的UI
app.registerExtension({
    name: "comfyui.feishu.table.ui",
    async beforeRegisterNodeType(nodeType, nodeData, app) {
        // 检查是否是飞书表格节点
        if (nodeData.name === "FeishuTableNode") {
            // 添加节点执行前的验证
            const originalOnExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                // 显示执行结果
                if (message && message.prompt) {
                    console.log("飞书表格节点执行完成:", message);
                }
                if (originalOnExecuted) {
                    originalOnExecuted.call(this, message);
                }
            };

            // 添加节点执行前的验证
            const originalOnExecuting = nodeType.prototype.onExecuting;
            nodeType.prototype.onExecuting = function(message) {
                // 验证输入参数
                const appId = this.widgets?.find(w => w.name === "app_id")?.value;
                const appSecret = this.widgets?.find(w => w.name === "app_secret")?.value;
                const tableUrl = this.widgets?.find(w => w.name === "table_url")?.value;

                if (!appId || !appSecret || !tableUrl) {
                    console.warn("飞书表格节点: 请填写完整的App ID、App Secret和表格链接");
                }

                if (originalOnExecuting) {
                    originalOnExecuting.call(this, message);
                }
            };
        }
    },

    async setup() {
        // 添加帮助提示
        const helpText = `
            <div style="padding: 10px; background: #f5f5f5; border-radius: 5px; margin: 10px 0;">
                <h4>飞书多维表格节点使用说明</h4>
                <p><strong>基本配置:</strong></p>
                <ul>
                    <li>App ID: 飞书应用的App ID</li>
                    <li>App Secret: 飞书应用的App Secret</li>
                    <li>表格链接: 飞书多维表格的完整链接</li>
                </ul>
                <p><strong>列筛选:</strong> 每行一个列名，留空表示获取所有列</p>
                <p><strong>条件筛选:</strong> 使用"列名=值"格式，每行一个条件</p>
                <p><strong>示例:</strong></p>
                <ul>
                    <li>列筛选: 重点内容\\n完成进度</li>
                    <li>条件筛选: 完成进度=未完成\\n负责人=张三</li>
                </ul>
            </div>
        `;

        // 在节点选择面板中添加帮助信息
        const nodeSelector = document.querySelector("#comfyui-node-selector");
        if (nodeSelector) {
            const helpDiv = document.createElement("div");
            helpDiv.innerHTML = helpText;
            helpDiv.style.display = "none";
            helpDiv.id = "feishu-table-help";
            nodeSelector.appendChild(helpDiv);

            // 添加帮助按钮
            const helpButton = document.createElement("button");
            helpButton.textContent = "飞书表格帮助";
            helpButton.style.cssText = "margin: 5px; padding: 5px 10px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;";
            helpButton.onclick = () => {
                const helpDiv = document.getElementById("feishu-table-help");
                if (helpDiv) {
                    helpDiv.style.display = helpDiv.style.display === "none" ? "block" : "none";
                }
            };
            nodeSelector.appendChild(helpButton);
        }
    }
});

// 添加节点执行状态指示器
app.registerExtension({
    name: "comfyui.feishu.table.status",
    async beforeRegisterNodeType(nodeType, nodeData, app) {
        if (nodeData.name === "FeishuTableNode") {
            // 添加状态指示器
            const originalGetSize = nodeType.prototype.getSize;
            nodeType.prototype.getSize = function() {
                const size = originalGetSize ? originalGetSize.call(this) : [200, 300];
                // 为状态指示器留出空间
                return [Math.max(size[0], 250), size[1] + 50];
            };

            // 添加状态显示
            const originalDrawForeground = nodeType.prototype.drawForeground;
            nodeType.prototype.drawForeground = function(ctx) {
                if (originalDrawForeground) {
                    originalDrawForeground.call(this, ctx);
                }

                // 绘制状态指示器
                const statusWidget = this.widgets?.find(w => w.name === "status_info");
                if (statusWidget && statusWidget.value) {
                    ctx.save();
                    ctx.font = "12px Arial";
                    ctx.fillStyle = "#666";
                    
                    // 根据状态显示不同颜色
                    if (statusWidget.value.includes("错误")) {
                        ctx.fillStyle = "#ff4444";
                    } else if (statusWidget.value.includes("成功")) {
                        ctx.fillStyle = "#44ff44";
                    }
                    
                    // 绘制状态文本
                    const lines = statusWidget.value.split('\n');
                    let y = this.size[1] - 30;
                    for (const line of lines) {
                        if (line.trim()) {
                            ctx.fillText(line.trim(), 10, y);
                            y += 15;
                        }
                    }
                    ctx.restore();
                }
            };
        }
    }
});

// 添加错误处理和重试机制
app.registerExtension({
    name: "comfyui.feishu.table.error-handling",
    async beforeRegisterNodeType(nodeType, nodeData, app) {
        if (nodeData.name === "FeishuTableNode") {
            // 添加重试按钮
            const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                if (originalOnNodeCreated) {
                    originalOnNodeCreated.call(this);
                }

                // 添加重试按钮
                const retryButton = {
                    name: "retry",
                    type: "button",
                    value: "重试",
                    callback: () => {
                        // 清除错误状态
                        const statusWidget = this.widgets?.find(w => w.name === "status_info");
                        if (statusWidget) {
                            statusWidget.value = "";
                        }
                        
                        // 重新执行节点
                        if (this.graph) {
                            this.graph.runStep(0, this.id);
                        }
                    }
                };

                // 将重试按钮添加到可选输入中
                if (this.widgets) {
                    this.widgets.push(retryButton);
                }
            };
        }
    }
});

console.log("飞书多维表格插件前端扩展已加载");
