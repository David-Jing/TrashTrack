from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient


class ComputerVision:
    def __init__(self):
        # Azure Custom Vision API Authentication
        self.ENDPOINT = "https://westus2.api.cognitive.microsoft.com/"
        self.prediction_key = "0f43b589cb784d5eb502ed57a47845df"
        self.project_id = "2da0b4f6-8909-42ea-b94a-d7e55cfffcc5"
        self.publish_iteration_name = "BeatDetection"

        # Prediction Fine Tuning
        self.min_confidence = 0.5
        self.line_heuristic = 0.2

    def __takeThird(self, elem):
        return elem[2]

    # Selection sort on subsection indexed a to b, sorting at index
    def __subSectionSort(self, notes, a, b, index):
        # print(a)
        # print(b)
        # print("------")
        for i in range(a, b+1):
            min_idx = i
            for j in range(i+1, b+1):
                if notes[min_idx][index] > notes[j][index]:
                    min_idx = j

            notes[i], notes[min_idx] = notes[min_idx], notes[i]

    # Grouping notes by line and sorting each group
    def __noteSort(self, notes):
        notes.sort(key=self.__takeThird)
        i, j = 0, 0
        for k in range(1, len(notes)):
            j += 1
            if i == j:
                continue
            elif notes[k][2] - notes[k-1][2] > self.line_heuristic:
                self.__subSectionSort(notes, i, j-1, 1)
                i = j

        self.__subSectionSort(notes, i, len(notes)-1, 1)

    # Returns list a sorted list of note type from a local sheet music image, sorted chronologically
    def localAnalysis(self, location):
        # Initialize Object Predictor
        predictor = CustomVisionPredictionClient(
            self.prediction_key, endpoint=self.ENDPOINT)

        # Open the sample image and get back the prediction results.
        with open(location, mode="rb") as test_data:
            results = predictor.detect_image(
                self.project_id, self.publish_iteration_name, test_data)

        # Display the results.
        notes = []
        for prediction in results.predictions:
            if prediction.probability > self.min_confidence:
                notes.append([prediction.tag_name, prediction.bounding_box.left,
                              prediction.bounding_box.top, prediction.probability])

        # Sort the data.
        self.__noteSort(notes)

        # print("Note, Left, Top, Prob")
        # for note in notes:
        #     print(note)

        output = []
        for note in notes:
            output.append(note[0])

        return output


A = ComputerVision()
B = A.localAnalysis("Capture.PNG")

print(B)
# B = A.localAnalysis("A-Minor-scale.png")
# B = A.localAnalysis("beginner-piano-sheet-tim-topham.png")
