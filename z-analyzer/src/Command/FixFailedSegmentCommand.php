<?php

namespace App\Command;

use App\Entity\FailedImportAttempt;
use App\Service\ImportProcessHandler;
use Doctrine\Common\Collections\ArrayCollection;
use Psr\Log\LoggerInterface;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use DateTime;

class FixFailedSegmentCommand extends Command
{
    protected static $defaultName = 'app:fix-failed-segment';
    private ContainerInterface $container;
    private LoggerInterface $logger;
    private ImportProcessHandler $processHandler;

    public function __construct(
        ContainerInterface $container,
        LoggerInterface $logger,
        ImportProcessHandler $processHandler
    ) {
        parent::__construct();
        $this->container = $container;
        $this->logger = $logger;
        $this->processHandler = $processHandler;
    }

    protected function configure()
    {
        $this
            ->setDescription('Command for retrying failed attempts')
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $doctrine = $this->container->get('doctrine');
        $manager = $doctrine->getManager();
        $attemptRepo = $manager->getRepository(FailedImportAttempt::class);

        /** @var ArrayCollection $failedAttempts */
        $failedAttempts = $attemptRepo->getAllNotRetried();
        $collection = new ArrayCollection();

        /** @var FailedImportAttempt $attempt */
        foreach ($failedAttempts->getValues() as $attempt) {
            if ($collection->contains($attempt->getCamera())) {
                $attempt->setRetried(true);
                continue;
            }
            $collection->add($attempt->getCamera());
            $attempt->setRetried(true);
        }
        $manager->flush();

        $this->processHandler->importFromCameras($collection);

        $timeNow = new DateTime();
        $message = '';
        $message .= '[' . $timeNow->format('Y-m-d H:i:s') . '] - ';
        $message .= 'Import Fix command completed';

        $this->logger->info($message);

        return 0;
    }
}
