<?php

namespace App\Command;

use App\Service\ImportProcessHandler;
use App\Entity\Segment;
use App\Utility\DBAL\Type\SegmentType;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Doctrine\ORM\EntityManagerInterface;
use Psr\Log\LoggerInterface;
use DateTime;

class SegmentImportCommand extends Command
{
    protected static $defaultName = 'app:segment-import';

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
            ->setDescription('Import segments with type as argument')
            ->addOption(
                'segment-type',
                null,
                InputOption::VALUE_REQUIRED,
                'Type of segment for import'
            )
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        $segmentType = $input->getOption('segment-type');

        if (!$this->validateSegment($segmentType)) {
            $io->error('Wrong segment type supplemented');
            return 1;
        }

        $doctrine = $this->container->get('doctrine');
        $manager = $doctrine->getManager();
        $segmentRepository = $manager->getRepository(Segment::class);
        /** @var Segment $segment */
        $segment = $segmentRepository->findOneBy(['type' => $segmentType]);
        $camerasCollection = $segment->getCameras();

        $this->processHandler->importFromCameras($camerasCollection);

        $timeNow = new DateTime();
        $message = '';
        $message .= '[' . $timeNow->format('Y-m-d H:i:s') . '] - ';
        $message .= $segmentType . ' - Import completed';

        $this->logger->info($message);

        return 0;
    }

    protected function validateSegment(string $segment): bool
    {
        return array_key_exists($segment, SegmentType::$choices);
    }
}
