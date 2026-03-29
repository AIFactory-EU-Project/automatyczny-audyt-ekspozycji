<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Tests\Service;

use App\Service\ProductGroupManager;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

/**
 * Class UserService.
 */
class ProductGroupManagerTest extends KernelTestCase
{
    public function setUp()
    {
        parent::setUp();
        self::bootKernel();
    }

    public function testServiceInit(): void
    {
        $productGroupManager = static::$kernel->getContainer()->get(ProductGroupManager::class);
        $this->assertInstanceOf(ProductGroupManager::class, $productGroupManager);
    }
}
