import urllib
import torch
import gradio as gr
import torchvision.transforms as T
import torch.nn.functional as F
import os

def main() :
    ckpt_path = "./model/model.script.pt"

    print("Running Demo")

    print("Instantiating scripted model: {}".format(ckpt_path))
    model = torch.jit.load(ckpt_path)

    print("Getting CIFAR10 class names...")
    # get the cifar10 classnames
    url, filename = (
        "<https://raw.githubusercontent.com/RubixML/CIFAR-10/master/labels.txt>",
        "labels.txt",
    )
    urllib.request.urlretrieve(url, filename)
    with open("labels.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    transforms = T.Compose(
            [T.ToTensor(), 
             T.Resize((32, 32)),
             T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
        )

    def predict(image):
        if image is None:
            return None
        image = transforms(image).unsqueeze(0)
        # image = torch.tensor(image[None, None, ...], dtype=torch.float32)
        logits = model(image)
        preds = F.softmax(logits, dim=1).squeeze(0).tolist()
        return {categories[i]: preds[i] for i in range(10)}

    demo = gr.Interface(
        fn=predict,
        inputs=gr.Image(type="pil"),
        outputs=[gr.Label(num_top_classes=10)],
        live=True,
        examples=[
        os.path.join(os.path.dirname(__file__), "sample/airplane.jpg"),
        os.path.join(os.path.dirname(__file__), "sample/car.jpg"),
        os.path.join(os.path.dirname(__file__), "sample/horse.jpg"),
        os.path.join(os.path.dirname(__file__), "sample/frog.jpg"),
        os.path.join(os.path.dirname(__file__), "sample/truck.jpg"),
    ]
    )

    print("Launching the web application...")
    demo.launch(server_name="0.0.0.0", server_port=8080)

if __name__ == "__main__":
    main()