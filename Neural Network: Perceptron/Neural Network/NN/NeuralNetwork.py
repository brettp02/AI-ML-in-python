import numpy as np


class Neural_Network:
    # Initialize the network
    def __init__(self, num_inputs, num_hidden, num_outputs, hidden_layer_weights, output_layer_weights, learning_rate):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        self.hidden_layer_weights = hidden_layer_weights
        self.output_layer_weights = output_layer_weights

        self.learning_rate = learning_rate

    # Calculate neuron activation for an input
    def sigmoid(self, input):
        output = 1 / (1 + np.exp(-input))  # TODO! / (COMPLETE)
        return output

    # Feed forward pass input to a network output
    def forward_pass(self, inputs):
        hidden_layer_outputs = []
        for i in range(self.num_hidden):
            # TODO! Calculate the weighted sum, and then compute the final output. (COMPLETE)
            weighted_sum = np.dot(inputs, self.hidden_layer_weights[:, i])
            output = self.sigmoid(weighted_sum)
            hidden_layer_outputs.append(output)
            #print(f"Hidden layer neuron {i + 1} weighted sum: {weighted_sum}, output: {output}")


        output_layer_outputs = []
        for i in range(self.num_outputs):
            # TODO! Calculate the weighted sum, and then compute the final output. (COMPLETE)
            weighted_sum = np.dot(hidden_layer_outputs, self.output_layer_weights[:, i])
            output = self.sigmoid(weighted_sum)
            output_layer_outputs.append(output)
            #print(f"Output layer neuron {i + 1} weighted sum: {weighted_sum}, output: {output}")

        return hidden_layer_outputs, output_layer_outputs


    # Backpropagate error and store in neurons
    def backward_propagate_error(self, inputs, hidden_layer_outputs, output_layer_outputs, desired_outputs):

        output_layer_betas = np.zeros(self.num_outputs)
        # TODO! Calculate output layer betas. (COMPLETE)
        output_layer_betas = desired_outputs - output_layer_outputs
        print('OL betas: ', output_layer_betas)

        hidden_layer_betas = np.zeros(self.num_hidden)
        # TODO! Calculate hidden layer betas.(COMPLETE)
        for i in range(self.num_hidden):
            for j in range(self.num_outputs):
                hidden_layer_betas[i] += output_layer_betas[j] * self.output_layer_weights[i,j]
            hidden_layer_betas[i] *= hidden_layer_outputs[i] * (1-hidden_layer_outputs[i])
        print('HL betas: ', hidden_layer_betas)

        # This is a HxO array (H hidden nodes, O outputs)
        delta_output_layer_weights = np.zeros((self.num_hidden, self.num_outputs))
        # TODO! Calculate output layer weight changes. (COMPLETE)
        for i in range(self.num_hidden):
            for j in range(self.num_outputs):
                delta_output_layer_weights[i, j] = output_layer_betas[j] * hidden_layer_outputs[i]

        # This is a IxH array (I inputs, H hidden nodes)
        delta_hidden_layer_weights = np.zeros((self.num_inputs, self.num_hidden))
        # TODO! Calculate hidden layer weight changes. (COMPLETE)
        for i in range(self.num_inputs):
            for j in range(self.num_hidden):
                delta_hidden_layer_weights[i, j] = hidden_layer_betas[j] * inputs[i]
        # Return the weights we calculated, so they can be used to update all the weights.

        return delta_output_layer_weights, delta_hidden_layer_weights

    def update_weights(self, delta_output_layer_weights, delta_hidden_layer_weights):
        # TODO! Update the weights. (COMPLETE)
        self.output_layer_weights += self.learning_rate * delta_output_layer_weights
        self.hidden_layer_weights += self.learning_rate * delta_hidden_layer_weights

    def train(self, instances, desired_outputs, epochs):
        #self.training_accuracy = []
        for epoch in range(epochs):
            print('epoch = ', epoch)
            predictions = []
            for i, instance in enumerate(instances):
                hidden_layer_outputs, output_layer_outputs = self.forward_pass(instance)
                delta_output_layer_weights, delta_hidden_layer_weights, = self.backward_propagate_error(
                    instance, hidden_layer_outputs, output_layer_outputs, desired_outputs[i])
                predicted_class = np.argmax(output_layer_outputs)  # TODO!
                predictions.append(predicted_class)

                # We use online learning, i.e. update the weights after every instance.
                self.update_weights(delta_output_layer_weights, delta_hidden_layer_weights)

            # Print new weights
            print('Hidden layer weights \n', self.hidden_layer_weights)
            print('Output layer weights  \n', self.output_layer_weights)

            # TODO: Print accuracy achieved over this epoch
            acc = np.mean(np.array(predictions) == np.argmax(desired_outputs, axis=1))
            #self.training_accuracy.append(acc)
            print('acc = ', acc)

    def predict(self, instances):
        predictions = []
        for instance in instances:
            hidden_layer_outputs, output_layer_outputs = self.forward_pass(instance)
            predicted_class = np.argmax(output_layer_outputs)  # TODO! Should be 0, 1, or 2.
            predictions.append(predicted_class)
        return predictions

