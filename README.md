<h1 align="center">FastAPI Replicate Model Trainer</h1>

<p align="center">
This repository provides a FastAPI-based application to automate model creation and training on the Replicate platform. The application accepts user-uploaded datasets in <code>.zip</code> format and integrates with Replicate's API to train fine-tuned models using the provided images.
</p>

<h2>🚀 Features</h2>

<ul>
  <li><b>User-Defined Model Creation</b>: Accepts a <code>username</code> as input to personalize model names for easy organization.</li>
  <li><b>Automated Training</b>: Uploads user-provided images in <code>.zip</code> format to Replicate and initiates training with customizable steps.</li>
  <li><b>Temporary File Handling</b>: Saves uploaded files temporarily for processing, then deletes them post-training to optimize storage.</li>
  <li><b>Error Handling</b>: Provides robust error messages and responses to ensure users are informed of any issues during model creation or training.</li>
  <li><b>API Endpoint</b>: Simple <code>/train</code> endpoint where users can upload datasets and trigger model training.</li>
</ul>

<h2>📋 Requirements</h2>

<ul>
  <li><b>FastAPI</b>: A modern, fast (high-performance) web framework for building APIs with Python 3.6+.</li>
  <li><b>Replicate API</b>: Used for model training and creation; requires a valid API token.</li>
  <li><b>Ngrok</b> (optional): Can be used to expose the local server for testing purposes.</li>
</ul>

<h2>⚙️ Getting Started</h2>

<ol>
  <li>Clone this repository.</li>
  <li>Set up environment variables with your Replicate API token.</li>
  <li>Start the FastAPI server and access the <code>/train</code> endpoint to upload a <code>.zip</code> file and begin training.</li>
</ol>

<h2>📄 Example Request</h2>

<p>Make a <code>POST</code> request to <code>/train</code> with a <code>.zip</code> file containing training images and a <code>username</code>. The application will respond with the model's name, initial training status, and a link to the training process on Replicate.</p>

<hr>

<p>This repository provides a convenient solution for users looking to quickly train and fine-tune models on Replicate using FastAPI. Feedback and contributions are welcome!</p>


