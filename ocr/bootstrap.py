def evaluate_conversion():
    from source.conversion.evaluate import Evaluator
    evaluator = Evaluator(100, subset_name='PRINTED_1561')
    # evaluator.get_correct_predictions_percent(
    #     '/tmp/ocr/eval20171002_175150.log')
    evaluator.start()
    evaluator.spectator()
    evaluator.join()


def convert_directories():
    from source.conversion.process import ProcessLineBuilder, \
        run_directory_processing
    from source.conversion.stages.utils import move_random_images_to_directory
    from source.config import cfg

    process_line = ProcessLineBuilder().process_line
    move_random_images_to_directory(20, cfg.ProcessLine.START_PATH,
                                    subset_name='printed_296')
    run_directory_processing(process_line)


def convert_dataset_to_png():
    from source.conversion.dataset import ImageFormatConverter
    import os
    from source.config import cfg

    dst_path = os.path.join(cfg.Root.DATA_PATH, 'private', 'png2')
    converter = ImageFormatConverter(dst_path=dst_path)
    converter.run_job()


def attention_ocr_training():
    from source.recognition.train import run_training
    run_training()


def attention_ocr_evaluation():
    from source.recognition.eval import run_evaluation
    run_evaluation()


def synth_database_generation():
    from source.conversion.tfrecords_conversion import SyntheticConverter
    SyntheticConverter(
        dataset_name='private_fsns',
        folder_name='private_fsns_dates_synth',
        size=50000,
        split='train'
    ).generate()


if __name__ == "__main__":
    # from source.recognition.train import main
    # attention_ocr_training()

    # from source.recognition.eval import main
    # attention_ocr_evaluation()

    synth_database_generation()
