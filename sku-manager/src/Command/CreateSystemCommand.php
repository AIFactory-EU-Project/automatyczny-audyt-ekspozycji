<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Command;

use App\Service\SystemManager;
use Exception;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

/**
 * Class CreateUserCommand.
 */
class CreateSystemCommand extends Command
{
    protected static $defaultName = 'app:create-system';

    private SystemManager $systemManager;

    /**
     * CreateSystemCommand constructor.
     *
     * @param SystemManager $systemManager
     */
    public function __construct(SystemManager $systemManager)
    {
        $this->systemManager = $systemManager;

        parent::__construct();
    }

    protected function configure()
    {
        $this->setDescription('Creates a new system.');
        $this->addArgument('name', InputArgument::REQUIRED, 'name');
        $this->addArgument('region', InputArgument::REQUIRED, 'region');
        $this->addArgument('contact', InputArgument::REQUIRED, 'contact email');
    }

    /**
     * @param InputInterface  $input
     * @param OutputInterface $output
     *
     * @return int
     *
     * @throws Exception
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $system = $this->systemManager->getNewSystem();
        $system->setName($input->getArgument('name'));
        $system->setRegion($input->getArgument('region'));
        $system->setContact($input->getArgument('contact'));
        $system->setActive(true);

        $errors = $this->systemManager->validateSystem($system);
        if ($errors->count()) {
            $output->writeln($errors);

            return 1;
        }

        $this->systemManager->addSystem($system);
        $output->writeln('System '.$input->getArgument('name').' created');

        return 0;
    }
}
