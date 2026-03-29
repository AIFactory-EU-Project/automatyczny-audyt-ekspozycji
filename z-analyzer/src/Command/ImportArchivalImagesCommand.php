<?php

namespace App\Command;

use App\Service\ImportProcessHandler;
use Psr\Log\LoggerInterface;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

class ImportArchivalImagesCommand extends Command
{
    protected static $defaultName = 'app:import-archival-images';
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

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $process = new Process(
            [
                '/usr/bin/python3',
                '/usr/src/app/bin/perspective_transformation.py',
                '"/usr/src/app/nowe_zdjecie.png"',
                '"172.16.11.252"',
                '"ready_meal"',
            ]
        );

        $process = Process::fromShellCommandline(
            '$python $scriptLocation "$imageLocation" "$ipAddress" "$segment"'
        );
        $end = $process->run(null, [
            'python' => '/usr/bin/python3',
            'scriptLocation' => '/usr/src/app/bin/perspective_transformation.py',
            'imageLocation' => '/usr/src/app/nowe_zdjecie.png',
            'ipAddress' => '172.16.11.252',
            'segment' => 'ready_meal',
        ]);

        $output->setVerbosity(OutputInterface::VERBOSITY_DEBUG);

        $output->write([
            $process->getOutput(),
            $process->getErrorOutput(),
            $end,
        ]);

        return $end;
    }
}
