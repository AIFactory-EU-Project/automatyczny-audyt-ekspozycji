<?php

namespace App\Command;

use App\Entity\File;
use App\Service\Uploader\LocalStorage;
use DateInterval;
use DateTime;
use App\Entity\Photo;
use Psr\Log\LoggerInterface;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class CleanOldFilesCommand extends Command
{
    protected static $defaultName = 'app:clean-old-files';

    private const FILE_EXPIRATION_TIMESPAN = 'P7D';

    private ContainerInterface $container;
    private LocalStorage $localStorage;
    private LoggerInterface $logger;


    public function __construct(
        ContainerInterface $container,
        LocalStorage $localStorage,
        LoggerInterface $logger
    ) {
        parent::__construct();
        $this->container = $container;
        $this->localStorage = $localStorage;
        $this->logger = $logger;
    }

    protected function configure()
    {
        $this
            ->setDescription('Remove temporary files (failed and successful) older than a month from local storage')
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $doctrineManager = $this->container->get('doctrine')->getManager();
        $photoRepository = $doctrineManager->getRepository(Photo::class);

        $dateNow = new DateTime();
        $dateLimit = $dateNow->sub(new DateInterval(self::FILE_EXPIRATION_TIMESPAN));

        $oldPhotos = $photoRepository->getLocalOlderThan($dateLimit);

        /** @var Photo $photo */
        foreach ($oldPhotos as $photo) {
            // TODO optimization - search for related temporary files first and associate them with photos
            $fileRepository = $doctrineManager->getRepository(File::class);
            /** @var File $file */
            $file = $fileRepository->find($photo->getStorageId());
            if ($file->isTemporary()) {
                $this->localStorage->removeFile($file);
                $doctrineManager->remove($photo);
            }
        }

        $timeNow = new DateTime();
        $message = '';
        $message .= '[' . $timeNow->format('Y-m-d H:i:s') . '] - ';
        $message .= 'Clean Old Files command completed';

        $this->logger->info($message);

        return 0;
    }
}
