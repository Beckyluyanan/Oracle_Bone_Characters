import gradio as gr
from MMEdu import MMClassification as cls

model = cls(backbone='LeNet')
checkpoint = 'best_accuracy_top-1_epoch_9.pth'
classes = ['人','大']

def instruct_and_predict(instruction, input_img=None):
    if input_img is None:
        return "", "请按照上方的指示开始绘图。"
    else:
        result = model.inference(image=input_img, show=False, checkpoint=checkpoint)
        result = model.print_result(result)
        result_text = classes[result[0]['标签']]
        feedback = ""
        if result[0]['置信度'] < 0.99:
            feedback = f"不太对哦，我都判断不准确了！"
        else:    
            if instruction == result_text:
                feedback = "恭喜！你画得很好！"
            else:
                feedback = f"不太对哦，我期望的是：{instruction}，但你画的像：{result_text}。"

        return result_text, feedback

label_input = gr.inputs.Textbox(default="", label="我希望你画的是")
Image_input = gr.inputs.Image(shape=(128, 128), source="canvas", label="画板", optional=True)
label_output = gr.outputs.Textbox(label="你画的甲骨文是")
Image_output = gr.outputs.Textbox(label="反馈")

demo = gr.Interface(fn=instruct_and_predict, 
    inputs=[label_input,Image_input],
    outputs=[label_output,Image_output],
    live=False,
    layout="vertical",
    title="甲骨文学习小游戏",
    description="请在上方文本框输入你希望绘制的甲骨文（例如：“人”或“大”），然后在画板上进行绘制，查看结果。",
    theme="huggingface"
)

demo.launch(share=True)