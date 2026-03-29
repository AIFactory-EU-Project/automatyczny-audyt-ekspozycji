<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Command;

use App\Service\SystemManager;
use App\Service\UserManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

/**
 * Class CreateUserCommand.
 */
class CreateUserCommand extends Command
{
    protected static $defaultName = 'app:create-user';

    private UserManager $userManager;
    private SystemManager $systemManager;

    /**
     * CreateUserCommand constructor.
     *
     * @param UserManager   $userManager
     * @param SystemManager $systemManager
     */
    public function __construct(UserManager $userManager, SystemManager $systemManager)
    {
        $this->userManager = $userManager;
        $this->systemManager = $systemManager;

        parent::__construct();
    }

    protected function configure()
    {
        $this->setDescription('Creates a new user.');
        $this->addArgument('email', InputArgument::REQUIRED, 'User email');
        $this->addArgument('system', InputArgument::REQUIRED, 'System');
        $this->addArgument('plainPassword', InputArgument::REQUIRED, 'plainPassword');
        $this->addArgument('role', InputArgument::OPTIONAL, 'role', null);
    }

    /**
     * @param InputInterface  $input
     * @param OutputInterface $output
     *
     * @return int
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    protected function execute(InputInterface $input, OutputInterface $output)
    {
        $system = $this->systemManager->getSystemByName($input->getArgument('system'));

        if (!$system) {
            $output->writeln('System '.$input->getArgument('system').' not found');

            return 1;
        }

        $user = $this->userManager->getNewUser($system);
        $user->setEmail($input->getArgument('email'));
        $user->setPlainPassword($input->getArgument('plainPassword'));
        $user->setActive(true);

        if ($input->getArgument('role')) {
            $roles = [$input->getArgument('role')];
            $user->setRoles($roles);
        }

        $errors = $this->userManager->validateUser($user);
        if ($errors->count()) {
            $output->writeln($errors);

            return 1;
        }

        $this->userManager->addUser($user);

        $output->writeln('User '.$input->getArgument('email').' created');

        return 0;
    }
}
